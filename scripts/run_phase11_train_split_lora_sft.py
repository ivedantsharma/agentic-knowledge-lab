import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from peft import (
    LoraConfig,
    TaskType,
    get_peft_model,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyAction,
    RetrievalPolicyExample,
    RetrievalPolicySplit,
    parse_retrieval_policy_action,
)
from knowledge_engine.training.sft_format import (
    build_policy_sft_text,
    build_target_only_labels,
)

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
DATA_PATH = Path(
    "data/processed/phase11_policy_dataset_v0.json"
)

EPOCHS = 2
LEARNING_RATE = 2e-4


def load_examples() -> list[RetrievalPolicyExample]:
    return [
        RetrievalPolicyExample.model_validate(item)
        for item in json.loads(
            DATA_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


def build_training_tensors(
    tokenizer: AutoTokenizer,
    example: RetrievalPolicyExample,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    formatted = build_policy_sft_text(
        question=example.question,
        target_action=example.target_action,
    )

    prompt_messages = [
        {
            "role": "system",
            "content": formatted.system_text,
        },
        {
            "role": "user",
            "content": formatted.user_text,
        },
    ]

    full_messages = [
        *prompt_messages,
        {
            "role": "assistant",
            "content": formatted.target_text,
        },
    ]

    prompt_ids = tokenizer.apply_chat_template(
        prompt_messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=False,
    )
    full_ids = tokenizer.apply_chat_template(
        full_messages,
        tokenize=True,
        add_generation_prompt=False,
        return_dict=False,
    )

    labels = build_target_only_labels(
        input_ids=full_ids,
        prompt_token_count=len(prompt_ids),
    )

    input_ids = torch.tensor(
        [full_ids],
        dtype=torch.long,
    )
    label_tensor = torch.tensor(
        [labels],
        dtype=torch.long,
    )
    attention_mask = torch.ones_like(
        input_ids
    )

    return (
        input_ids,
        attention_mask,
        label_tensor,
    )


def generate_action(
    tokenizer: AutoTokenizer,
    model: torch.nn.Module,
    example: RetrievalPolicyExample,
) -> tuple[str, RetrievalPolicyAction | None]:
    formatted = build_policy_sft_text(
        question=example.question,
        target_action=example.target_action,
    )

    messages = [
        {
            "role": "system",
            "content": formatted.system_text,
        },
        {
            "role": "user",
            "content": formatted.user_text,
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=16,
            do_sample=False,
        )

    generated_ids = output_ids[
        :,
        inputs["input_ids"].shape[1] :,
    ]

    raw = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )[0].strip()

    return (
        raw,
        parse_retrieval_policy_action(raw),
    )


def evaluate(
    tokenizer: AutoTokenizer,
    model: torch.nn.Module,
    examples: list[RetrievalPolicyExample],
    label: str,
) -> dict[str, float]:
    model.eval()

    correct = 0
    parseable = 0
    predicted_counts: Counter[str] = Counter()

    print(label)

    for example in examples:
        raw, predicted = generate_action(
            tokenizer,
            model,
            example,
        )

        is_correct = (
            predicted == example.target_action
        )
        is_parseable = predicted is not None

        correct += int(is_correct)
        parseable += int(is_parseable)

        predicted_counts[
            predicted.value
            if predicted is not None
            else "UNPARSEABLE"
        ] += 1

        print(
            f"  {example.example_id}: "
            f"target={example.target_action.value} "
            f"predicted="
            f"{predicted.value if predicted else None} "
            f"raw={raw!r} "
            f"correct={is_correct}"
        )

    total = len(examples)
    accuracy = correct / total
    format_compliance = parseable / total

    print(
        f"  accuracy={accuracy:.4f}"
    )
    print(
        "  format_compliance="
        f"{format_compliance:.4f}"
    )
    print(
        "  predicted_counts="
        f"{dict(predicted_counts)}"
    )
    print()

    return {
        "accuracy": accuracy,
        "format_compliance": format_compliance,
    }


def main() -> None:
    torch.manual_seed(0)

    examples = load_examples()

    train_examples = [
        example
        for example in examples
        if example.split
        == RetrievalPolicySplit.TRAIN
    ]
    dev_examples = [
        example
        for example in examples
        if example.split
        == RetrievalPolicySplit.DEV
    ]
    heldout_examples = [
        example
        for example in examples
        if example.split
        == RetrievalPolicySplit.HELDOUT
    ]

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME
    )

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=4,
        lora_alpha=8,
        lora_dropout=0.0,
        bias="none",
        target_modules=[
            "q_proj",
            "v_proj",
        ],
    )

    model = get_peft_model(
        base_model,
        lora_config,
    )

    print(
        "Phase 11 EXP-105 — Train-Split LoRA SFT"
    )
    print(f"model={MODEL_NAME}")
    print(f"epochs={EPOCHS}")
    print(f"learning_rate={LEARNING_RATE}")
    print(
        f"train_examples={len(train_examples)}"
    )
    print(
        f"dev_examples={len(dev_examples)}"
    )
    print(
        "heldout_examples="
        f"{len(heldout_examples)}"
    )
    print()

    print("Before training")
    before_train = evaluate(
        tokenizer,
        model,
        train_examples,
        "TRAIN",
    )
    before_dev = evaluate(
        tokenizer,
        model,
        dev_examples,
        "DEV",
    )
    before_heldout = evaluate(
        tokenizer,
        model,
        heldout_examples,
        "HELDOUT",
    )

    optimizer = torch.optim.AdamW(
        (
            parameter
            for parameter in model.parameters()
            if parameter.requires_grad
        ),
        lr=LEARNING_RATE,
    )

    print("Training")
    model.train()

    epoch_mean_losses = []

    for epoch in range(
        1,
        EPOCHS + 1,
    ):
        losses = []

        for example in train_examples:
            (
                input_ids,
                attention_mask,
                labels,
            ) = build_training_tensors(
                tokenizer,
                example,
            )

            optimizer.zero_grad()

            output = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels,
            )
            loss = output.loss

            loss.backward()
            optimizer.step()

            losses.append(
                loss.item()
            )

        mean_loss = (
            sum(losses)
            / len(losses)
        )
        epoch_mean_losses.append(mean_loss)

        print(
            f"  epoch={epoch} "
            f"mean_train_loss={mean_loss:.6f}"
        )

    print()
    print("After training")
    after_train = evaluate(
        tokenizer,
        model,
        train_examples,
        "TRAIN",
    )
    after_dev = evaluate(
        tokenizer,
        model,
        dev_examples,
        "DEV",
    )
    after_heldout = evaluate(
        tokenizer,
        model,
        heldout_examples,
        "HELDOUT",
    )

    print("Summary")
    print(
        "  epoch_mean_losses="
        f"{epoch_mean_losses}"
    )
    print(
        "  train_accuracy_delta="
        f"{after_train['accuracy'] - before_train['accuracy']:.4f}"
    )
    print(
        "  dev_accuracy_delta="
        f"{after_dev['accuracy'] - before_dev['accuracy']:.4f}"
    )
    print(
        "  heldout_accuracy_delta="
        f"{after_heldout['accuracy'] - before_heldout['accuracy']:.4f}"
    )


if __name__ == "__main__":
    main()
