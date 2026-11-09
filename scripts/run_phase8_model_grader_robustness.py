import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.qwen_relation_verifier import (
    QwenRelationVerifier,
)

CASES_PATH = Path(
    "data/processed/phase8_relation_grader_robustness_v0.json"
)
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


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

    pair_predictions: dict[
        str,
        list[tuple[str, bool | None, bool]],
    ] = defaultdict(list)

    correct = 0
    format_errors = 0

    print(
        "Phase 8 EXP-081 — Model Grader "
        "Robustness and Disagreement Analysis"
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

        is_correct = (
            predicted == expected
            if predicted is not None
            else False
        )
        correct += is_correct

        pair_predictions[
            case["pair_id"]
        ].append(
            (
                case["variant"],
                predicted,
                expected,
            )
        )

        print(case["case_id"])
        print(
            f"  pair_id={case['pair_id']}"
        )
        print(
            f"  variant={case['variant']}"
        )
        print(
            f"  expected={expected}"
        )
        print(
            f"  predicted={predicted}"
        )
        print(
            f"  correct={is_correct}"
        )
        print(
            f"  format_error={error!r}"
        )
        print()

    print("Pair consistency")
    for pair_id, rows in pair_predictions.items():
        positive_predictions = [
            predicted
            for variant, predicted, expected in rows
            if expected
        ]
        stable_positive = (
            len(set(positive_predictions)) == 1
            if positive_predictions
            else True
        )

        print(pair_id)
        print(
            "  positive_predictions="
            f"{positive_predictions}"
        )
        print(
            f"  stable_positive={stable_positive}"
        )

    print()
    print("Aggregate")
    print(f"  cases={len(cases)}")
    print(
        f"  format_errors={format_errors}"
    )
    print(
        "  accuracy="
        f"{correct / len(cases):.4f}"
    )


if __name__ == "__main__":
    main()
