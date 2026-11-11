import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.calibrated_semantic_instruction_detector import (
    CalibratedSemanticInstructionDetector,
)
from knowledge_engine.agent.semantic_instruction_detector import (
    SemanticInstructionDetector,
)

CASES_PATH = Path(
    "data/processed/phase9_instruction_classifier_probe_v0.json"
)


def evaluate_detector(
    name: str,
    detector,
    spans: list[dict],
) -> dict[str, float | int]:
    tp = tn = fp = fn = 0
    by_category = defaultdict(
        lambda: {"correct": 0, "count": 0}
    )

    print(name)

    for case in spans:
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
                tp += 1
            else:
                fn += 1
        else:
            if predicted == "DATA":
                tn += 1
            else:
                fp += 1

        print(case["span_id"])
        print(f"  expected={expected}")
        print(f"  predicted={predicted}")
        print(f"  correct={correct}")

    total = len(spans)
    accuracy = (tp + tn) / total
    precision = (
        tp / (tp + fp)
        if tp + fp
        else 0.0
    )
    recall = (
        tp / (tp + fn)
        if tp + fn
        else 0.0
    )
    data_recall = (
        tn / (tn + fp)
        if tn + fp
        else 0.0
    )

    print("Aggregate")
    print(f"  true_positive={tp}")
    print(f"  true_negative={tn}")
    print(f"  false_positive={fp}")
    print(f"  false_negative={fn}")
    print(f"  accuracy={accuracy:.4f}")
    print(
        f"  instruction_precision={precision:.4f}"
    )
    print(
        f"  instruction_recall={recall:.4f}"
    )
    print(
        f"  data_recall={data_recall:.4f}"
    )
    print()

    return {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "data_recall": data_recall,
    }


def main() -> None:
    payload = json.loads(
        CASES_PATH.read_text(
            encoding="utf-8"
        )
    )
    model_name = payload["model"]
    spans = payload["spans"]

    baseline = SemanticInstructionDetector(
        model_name=model_name
    )
    calibrated = CalibratedSemanticInstructionDetector(
        model_name=model_name
    )

    print(
        "Phase 9 EXP-091 — Semantic Instruction "
        "Detector Prompt Calibration"
    )
    print(f"model={model_name}")
    print()

    baseline_metrics = evaluate_detector(
        "baseline",
        baseline,
        spans,
    )
    calibrated_metrics = evaluate_detector(
        "calibrated",
        calibrated,
        spans,
    )

    print("Delta")
    print(
        "  accuracy_delta="
        f"{calibrated_metrics['accuracy'] - baseline_metrics['accuracy']:.4f}"
    )
    print(
        "  instruction_precision_delta="
        f"{calibrated_metrics['precision'] - baseline_metrics['precision']:.4f}"
    )
    print(
        "  instruction_recall_delta="
        f"{calibrated_metrics['recall'] - baseline_metrics['recall']:.4f}"
    )
    print(
        "  data_recall_delta="
        f"{calibrated_metrics['data_recall'] - baseline_metrics['data_recall']:.4f}"
    )


if __name__ == "__main__":
    main()
