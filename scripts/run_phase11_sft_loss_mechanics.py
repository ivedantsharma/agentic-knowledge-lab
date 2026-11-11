import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyExample,
    RetrievalPolicySplit,
)
from knowledge_engine.training.sft_format import (
    build_policy_sft_text,
    build_target_only_labels,
    count_supervised_tokens,
)


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
DATA_PATH = Path(
    "data/processed/phase11_policy_dataset_v0.json"
)


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


def main() -> None:
    example = load_first_train_example()

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME
    )
    model.eval()

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
    )

    full_ids = tokenizer.apply_chat_template(
        full_messages,
        tokenize=True,
        add_generation_prompt=False,
    )

    labels = build_target_only_labels(
        input_ids=full_ids,
        prompt_token_count=len(prompt_ids),
    )

    supervised_ids = [
        token_id
        for token_id, label
        in zip(full_ids, labels)
        if label != -100
    ]

    input_tensor = torch.tensor(
        [full_ids],
        dtype=torch.long,
    )
    label_tensor = torch.tensor(
        [labels],
        dtype=torch.long,
    )

    with torch.no_grad():
        masked_output = model(
            input_ids=input_tensor,
            labels=label_tensor,
        )
        unmasked_output = model(
            input_ids=input_tensor,
            labels=input_tensor,
        )

    print(
        "Phase 11 EXP-103 — Causal-LM "
        "Target-Only Loss Mechanics"
    )
    print(f"model={MODEL_NAME}")
    print(f"example_id={example.example_id}")
    print(
        f"target={example.target_action.value}"
    )
    print()
    print("Token counts")
    print(
        f"  prompt_tokens={len(prompt_ids)}"
    )
    print(
        f"  full_tokens={len(full_ids)}"
    )
    print(
        "  supervised_tokens="
        f"{count_supervised_tokens(labels)}"
    )
    print(
        "  masked_prompt_tokens="
        f"{labels.count(-100)}"
    )
    print()
    print(
        "supervised_decode="
        f"{tokenizer.decode(supervised_ids)!r}"
    )
    print()
    print(
        "target_only_loss="
        f"{masked_output.loss.item():.6f}"
    )
    print(
        "unmasked_full_sequence_loss="
        f"{unmasked_output.loss.item():.6f}"
    )


if __name__ == "__main__":
    main()
