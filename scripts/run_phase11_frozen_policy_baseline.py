import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)

from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyAction,
    RetrievalPolicyExample,
    parse_retrieval_policy_action,
)


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
DATA_PATH = Path(
    "data/processed/phase11_policy_seed_v0.json"
)


def load_examples() -> list[RetrievalPolicyExample]:
    return [
        RetrievalPolicyExample.model_validate(item)
        for item in json.loads(
            DATA_PATH.read_text(
                encoding="utf-8"
            )
        )
    ]


def generate_action(
    tokenizer: AutoTokenizer,
    model: AutoModelForCausalLM,
    question: str,
) -> str:
    allowed = ", ".join(
        action.value
        for action in RetrievalPolicyAction
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a retrieval-policy classifier. "
                "Return exactly one allowed action token and "
                "nothing else."
            ),
        },
        {
            "role": "user",
            "content": (
                "Choose the retrieval action for the query.\n"
                "Action meanings:\n"
                "SEARCH_HYBRID_K1 = retrieve 1 candidate.\n"
                "SEARCH_HYBRID_K2 = retrieve 2 candidates.\n"
                "SEARCH_HYBRID_K3 = retrieve 3 candidates.\n"
                "SEARCH_HYBRID_K5 = retrieve 5 candidates.\n"
                "REFORMULATE = the query needs decomposition or "
                "rewriting before more retrieval.\n"
                f"Allowed actions: {allowed}\n"
                f"Query: {question}"
            ),
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

    output_ids = model.generate(
        **inputs,
        max_new_tokens=16,
        do_sample=False,
    )

    generated_ids = output_ids[
        :,
        inputs["input_ids"].shape[1] :,
    ]

    return tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )[0].strip()


def main() -> None:
    examples = load_examples()

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME
    )

    correct = 0
    parseable = 0
    predicted_counts: Counter[str] = Counter()

    print(
        "Phase 11 EXP-101 — Frozen Retrieval "
        "Policy Baseline"
    )
    print(f"model={MODEL_NAME}")
    print(f"examples={len(examples)}")
    print()

    for example in examples:
        raw_output = generate_action(
            tokenizer,
            model,
            example.question,
        )
        predicted = parse_retrieval_policy_action(
            raw_output
        )

        is_parseable = predicted is not None
        is_correct = (
            predicted == example.target_action
        )

        parseable += int(is_parseable)
        correct += int(is_correct)

        if predicted is not None:
            predicted_counts[predicted.value] += 1
        else:
            predicted_counts["UNPARSEABLE"] += 1

        print(example.example_id)
        print(
            f"  task={example.source_task_id}"
        )
        print(
            f"  target={example.target_action.value}"
        )
        print(
            f"  raw_output={raw_output!r}"
        )
        print(
            "  parsed="
            f"{predicted.value if predicted else None}"
        )
        print(f"  correct={is_correct}")
        print()

    total = len(examples)

    print("Aggregate")
    print(
        "  format_compliance="
        f"{parseable / total:.4f}"
    )
    print(
        "  action_accuracy="
        f"{correct / total:.4f}"
    )
    print(
        "  predicted_counts="
        f"{dict(predicted_counts)}"
    )


if __name__ == "__main__":
    main()
