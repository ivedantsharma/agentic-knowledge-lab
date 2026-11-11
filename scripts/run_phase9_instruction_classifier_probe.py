import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.semantic_instruction_detector import (
    SemanticInstructionDetector,
)


CASES_PATH = Path(
    "data/processed/phase9_instruction_classifier_probe_v0.json"
)


def main() -> None:
    payload = json.loads(
        CASES_PATH.read_text(
            encoding="utf-8"
        )
    )

    detector = SemanticInstructionDetector(
        model_name=payload["model"]
    )

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    by_category = defaultdict(
        lambda: {
            "correct": 0,
            "count": 0,
        }
    )

    print(
        "Phase 9 EXP-090 — Semantic Instruction "
        "Detector Classification Probe"
    )
    print(f"model={payload['model']}")
    print()

    for case in payload["spans"]:
        predicted_instruction = detector.is_instruction(
            case["text"]
        )
        predicted = (
            "INSTRUCTION"
            if predicted_instruction
            else "DATA"
        )
        expected = case["label"]
        correct = predicted == expected

        by_category[case["category"]]["count"] += 1
        by_category[case["category"]]["correct"] += int(
            correct
        )

        if expected == "INSTRUCTION":
            if predicted == "INSTRUCTION":
                true_positive += 1
            else:
                false_negative += 1
        else:
            if predicted == "DATA":
                true_negative += 1
            else:
                false_positive += 1

        print(case["span_id"])
        print(f"  category={case['category']}")
        print(f"  expected={expected}")
        print(f"  predicted={predicted}")
        print(f"  correct={correct}")
        print(f"  text={case['text']!r}")
        print()

    total = len(payload["spans"])
    accuracy = (
        true_positive + true_negative
    ) / total

    instruction_precision = (
        true_positive
        / (true_positive + false_positive)
        if true_positive + false_positive
        else 0.0
    )
    instruction_recall = (
        true_positive
        / (true_positive + false_negative)
        if true_positive + false_negative
        else 0.0
    )
    data_recall = (
        true_negative
        / (true_negative + false_positive)
        if true_negative + false_positive
        else 0.0
    )

    print("By category")
    for category, values in by_category.items():
        print(category)
        print(
            "  accuracy="
            f"{values['correct'] / values['count']:.4f}"
        )

    print()
    print("Aggregate")
    print(f"  true_positive={true_positive}")
    print(f"  true_negative={true_negative}")
    print(f"  false_positive={false_positive}")
    print(f"  false_negative={false_negative}")
    print(f"  accuracy={accuracy:.4f}")
    print(
        "  instruction_precision="
        f"{instruction_precision:.4f}"
    )
    print(
        "  instruction_recall="
        f"{instruction_recall:.4f}"
    )
    print(
        f"  data_recall={data_recall:.4f}"
    )


if __name__ == "__main__":
    main()
