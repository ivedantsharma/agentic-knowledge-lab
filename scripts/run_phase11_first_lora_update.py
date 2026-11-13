import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)

try:
    from peft import (
        LoraConfig,
        TaskType,
        get_peft_model,
    )
except ImportError as exc:
    raise RuntimeError(
        "EXP-104 requires PEFT. Install the pinned "
        "experiment dependency with: "
        "uv add peft==0.21.2"
    ) from exc

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyExample,
    RetrievalPolicySplit,
)
from knowledge_engine.training.sft_format import (
    build_policy_sft_text,
    build_target_only_labels,
)

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
DATA_PATH = Path(
    "data/processed/phase11_policy_dataset_v0.json"
)

TRAINING_STEPS = 3
LEARNING_RATE = 5e-4


def load_first_train_example() -> RetrievalPolicyExample:
    examples = [
        RetrievalPolicyExample.model_validate(item)
        for item in json.loads(
            DATA_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]

    return next(
        example
        for example in examples
        if example.split == RetrievalPolicySplit.TRAIN
    )


def build_example_tensors(
    tokenizer: AutoTokenizer,
    example: RetrievalPolicyExample,
) -> tuple[torch.Tensor, torch.Tensor]:
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

    return (
        torch.tensor(
            [full_ids],
            dtype=torch.long,
        ),
        torch.tensor(
            [labels],
            dtype=torch.long,
        ),
    )


def count_parameters(
    model: torch.nn.Module,
) -> tuple[int, int]:
    total = sum(
        parameter.numel()
        for parameter in model.parameters()
    )
    trainable = sum(
        parameter.numel()
        for parameter in model.parameters()
        if parameter.requires_grad
    )
    return total, trainable


def main() -> None:
    torch.manual_seed(0)

    example = load_first_train_example()

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

    total_params, trainable_params = (
        count_parameters(model)
    )

    input_ids, labels = build_example_tensors(
        tokenizer,
        example,
    )
    attention_mask = torch.ones_like(
        input_ids
    )

    model.eval()
    with torch.no_grad():
        initial_loss = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        ).loss.item()

    optimizer = torch.optim.AdamW(
        (
            parameter
            for parameter in model.parameters()
            if parameter.requires_grad
        ),
        lr=LEARNING_RATE,
    )

    step_losses = []

    model.train()

    for step in range(
        1,
        TRAINING_STEPS + 1,
    ):
        optimizer.zero_grad()

        output = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        )
        loss = output.loss

        loss.backward()
        optimizer.step()

        step_loss = loss.item()
        step_losses.append(step_loss)

        print(
            f"step={step} "
            f"training_loss={step_loss:.6f}"
        )

    model.eval()
    with torch.no_grad():
        final_loss = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        ).loss.item()

    print()
    print(
        "Phase 11 EXP-104 — First LoRA "
        "Parameter Update"
    )
    print(f"model={MODEL_NAME}")
    print(f"example_id={example.example_id}")
    print(
        f"target={example.target_action.value}"
    )
    print(
        f"training_steps={TRAINING_STEPS}"
    )
    print(
        f"learning_rate={LEARNING_RATE}"
    )
    print(
        f"total_parameters={total_params}"
    )
    print(
        f"trainable_parameters={trainable_params}"
    )
    print(
        "trainable_fraction="
        f"{trainable_params / total_params:.8f}"
    )
    print(
        f"initial_loss={initial_loss:.6f}"
    )
    print(
        f"final_loss={final_loss:.6f}"
    )
    print(
        "loss_delta="
        f"{final_loss - initial_loss:.6f}"
    )
    print(
        f"step_losses={step_losses}"
    )


if __name__ == "__main__":
    main()
