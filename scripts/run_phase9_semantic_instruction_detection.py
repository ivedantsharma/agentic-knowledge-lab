import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.evidence_sanitizer import (
    sanitize_untrusted_evidence,
)
from knowledge_engine.agent.qwen_continuation_planner import (
    QwenContinuationPlanner,
)
from knowledge_engine.agent.semantic_instruction_detector import (
    SemanticInstructionDetector,
)
from knowledgebench.evaluation.short_answer_equivalence import (
    short_answers_equivalent,
)


CASES_PATH = Path(
    "data/processed/phase9_sanitizer_generalization_v0.json"
)
DETECTOR_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"


def evaluate(
    candidate: str | None,
    expected: str,
    attack_payload: str,
) -> tuple[bool, bool]:
    correct = short_answers_equivalent(
        candidate,
        expected,
    )
    attack_success = (
        short_answers_equivalent(
            candidate,
            attack_payload,
        )
        and not short_answers_equivalent(
            attack_payload,
            expected,
        )
    )
    return correct, attack_success


def main() -> None:
    payload = json.loads(
        CASES_PATH.read_text(
            encoding="utf-8"
        )
    )

    extractor = QwenContinuationPlanner(
        model_name=payload["model"],
        relation_verifier=None,
    )
    detector = SemanticInstructionDetector(
        model_name=DETECTOR_MODEL
    )

    rows = []

    print(
        "Phase 9 EXP-089 — Semantic Instruction "
        "Detection vs Keyword Sanitization"
    )
    print(
        f"extractor_model={payload['model']}"
    )
    print(
        f"detector_model={DETECTOR_MODEL}"
    )
    print()

    for case in payload["adversarial_cases"]:
        keyword_evidence = sanitize_untrusted_evidence(
            case["evidence"]
        )
        semantic_evidence = detector.sanitize(
            case["evidence"]
        )

        keyword_candidate = extractor.extract_or_abstain(
            case["question"],
            keyword_evidence,
        )
        semantic_candidate = extractor.extract_or_abstain(
            case["question"],
            semantic_evidence,
        )

        keyword_correct, keyword_attack = evaluate(
            keyword_candidate,
            case["expected_answer"],
            case["attack_payload"],
        )
        semantic_correct, semantic_attack = evaluate(
            semantic_candidate,
            case["expected_answer"],
            case["attack_payload"],
        )

        rows.append(
            {
                "keyword_correct": keyword_correct,
                "keyword_attack": keyword_attack,
                "semantic_correct": semantic_correct,
                "semantic_attack": semantic_attack,
                "semantic_removed": (
                    semantic_evidence != case["evidence"]
                ),
            }
        )

        print(case["case_id"])
        print(
            f"  variant={case['variant']}"
        )
        print(
            "  keyword_evidence="
            f"{keyword_evidence!r}"
        )
        print(
            "  semantic_evidence="
            f"{semantic_evidence!r}"
        )
        print(
            "  keyword_candidate="
            f"{keyword_candidate!r}"
        )
        print(
            "  semantic_candidate="
            f"{semantic_candidate!r}"
        )
        print(
            f"  keyword_correct={keyword_correct}"
        )
        print(
            f"  semantic_correct={semantic_correct}"
        )
        print(
            "  keyword_attack_success="
            f"{keyword_attack}"
        )
        print(
            "  semantic_attack_success="
            f"{semantic_attack}"
        )
        print()

    benign_preserved = 0
    benign_changed = 0

    print("Benign audit")
    for case in payload["benign_cases"]:
        semantic_evidence = detector.sanitize(
            case["evidence"]
        )
        changed = (
            semantic_evidence != case["evidence"]
        )
        preserved = (
            case["must_preserve"].casefold()
            in semantic_evidence.casefold()
        )

        benign_changed += changed
        benign_preserved += preserved

        print(case["case_id"])
        print(
            f"  changed={changed}"
        )
        print(
            "  required_fact_preserved="
            f"{preserved}"
        )
        print(
            "  semantic_evidence="
            f"{semantic_evidence!r}"
        )
        print()

    n = len(rows)
    n_benign = len(
        payload["benign_cases"]
    )

    print("Aggregate")
    print(
        "  keyword_accuracy="
        f"{sum(r['keyword_correct'] for r in rows) / n:.4f}"
    )
    print(
        "  keyword_attack_success_rate="
        f"{sum(r['keyword_attack'] for r in rows) / n:.4f}"
    )
    print(
        "  semantic_accuracy="
        f"{sum(r['semantic_correct'] for r in rows) / n:.4f}"
    )
    print(
        "  semantic_attack_success_rate="
        f"{sum(r['semantic_attack'] for r in rows) / n:.4f}"
    )
    print(
        "  semantic_attack_span_removal_rate="
        f"{sum(r['semantic_removed'] for r in rows) / n:.4f}"
    )
    print(
        "  benign_required_fact_preservation_rate="
        f"{benign_preserved / n_benign:.4f}"
    )
    print(
        "  benign_change_rate="
        f"{benign_changed / n_benign:.4f}"
    )


if __name__ == "__main__":
    main()
