import json
from pathlib import Path

from knowledge_engine.agent.qwen_relation_verifier import (
    QwenRelationVerifier,
)


CASES_PATH = Path(
    "data/processed/phase8_relation_grader_cases_v0.json"
)
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


def safe_divide(
    numerator: int,
    denominator: int,
) -> float:
    return (
        numerator / denominator
        if denominator
        else 0.0
    )


def main() -> None:
    payload = json.loads(
        CASES_PATH.read_text(
            encoding="utf-8"
        )
    )
    cases = payload["cases"]

    verifier = QwenRelationVerifier(
        model_name=MODEL_NAME
    )

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    format_errors = 0

    print(
        "Phase 8 EXP-080 — Model Grader "
        "vs Deterministic Gold"
    )

    for case in cases:
        expected = case[
            "expected_relation_aligned"
        ]

        try:
            predicted = verifier.verify(
                question=case["question"],
                evidence=case["evidence"],
                candidate_answer=case[
                    "candidate_answer"
                ],
            )
            error = None
        except ValueError as exc:
            predicted = None
            error = str(exc)
            format_errors += 1

        if predicted is not None:
            if expected and predicted:
                true_positive += 1
            elif not expected and not predicted:
                true_negative += 1
            elif not expected and predicted:
                false_positive += 1
            elif expected and not predicted:
                false_negative += 1

        print(case["case_id"])
        print(
            f"  category={case['category']}"
        )
        print(
            f"  expected={expected}"
        )
        print(
            f"  predicted={predicted}"
        )
        print(
            f"  correct={predicted == expected}"
        )
        print(
            f"  format_error={error!r}"
        )
        print()

    valid_predictions = (
        len(cases) - format_errors
    )
    correct_predictions = (
        true_positive + true_negative
    )

    accuracy = safe_divide(
        correct_predictions,
        valid_predictions,
    )
    precision = safe_divide(
        true_positive,
        true_positive + false_positive,
    )
    recall = safe_divide(
        true_positive,
        true_positive + false_negative,
    )
    negative_accuracy = safe_divide(
        true_negative,
        true_negative + false_positive,
    )

    print("Aggregate")
    print(f"  cases={len(cases)}")
    print(
        f"  valid_predictions={valid_predictions}"
    )
    print(
        f"  format_errors={format_errors}"
    )
    print(
        f"  true_positive={true_positive}"
    )
    print(
        f"  true_negative={true_negative}"
    )
    print(
        f"  false_positive={false_positive}"
    )
    print(
        f"  false_negative={false_negative}"
    )
    print(
        f"  accuracy={accuracy:.4f}"
    )
    print(
        f"  positive_precision={precision:.4f}"
    )
    print(
        f"  positive_recall={recall:.4f}"
    )
    print(
        "  negative_accuracy="
        f"{negative_accuracy:.4f}"
    )


if __name__ == "__main__":
    main()
