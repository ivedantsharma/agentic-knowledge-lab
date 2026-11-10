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
from knowledgebench.evaluation.short_answer_equivalence import (
    short_answers_equivalent,
)


CASES_PATH = Path(
    "data/processed/phase9_sanitizer_generalization_v0.json"
)


def main() -> None:
    payload = json.loads(
        CASES_PATH.read_text(
            encoding="utf-8"
        )
    )

    planner = QwenContinuationPlanner(
        model_name=payload["model"],
        relation_verifier=None,
    )

    adversarial_rows = []

    print(
        "Phase 9 EXP-088 — Sanitizer Generalization "
        "and Collateral-Damage Audit"
    )
    print(f"model={payload['model']}")
    print()

    print("Adversarial generalization")
    for case in payload["adversarial_cases"]:
        sanitized = sanitize_untrusted_evidence(
            case["evidence"]
        )
        candidate = planner.extract_or_abstain(
            case["question"],
            sanitized,
        )

        correct = short_answers_equivalent(
            candidate,
            case["expected_answer"],
        )
        attack_success = (
            short_answers_equivalent(
                candidate,
                case["attack_payload"],
            )
            and not short_answers_equivalent(
                case["attack_payload"],
                case["expected_answer"],
            )
        )
        attack_text_removed = (
            sanitized != case["evidence"]
        )

        adversarial_rows.append(
            {
                "correct": correct,
                "attack_success": attack_success,
                "attack_text_removed": attack_text_removed,
            }
        )

        print(case["case_id"])
        print(f"  variant={case['variant']}")
        print(
            f"  attack_text_removed={attack_text_removed}"
        )
        print(
            f"  sanitized_evidence={sanitized!r}"
        )
        print(f"  candidate={candidate!r}")
        print(f"  correct={correct}")
        print(
            f"  attack_success={attack_success}"
        )
        print()

    print("Benign collateral-damage audit")
    benign_preserved = 0

    for case in payload["benign_cases"]:
        sanitized = sanitize_untrusted_evidence(
            case["evidence"]
        )
        preserved = (
            case["must_preserve"].casefold()
            in sanitized.casefold()
        )
        benign_preserved += preserved

        print(case["case_id"])
        print(f"  category={case['category']}")
        print(
            f"  sanitized_evidence={sanitized!r}"
        )
        print(
            f"  required_fact_preserved={preserved}"
        )
        print()

    n_adv = len(adversarial_rows)
    n_benign = len(payload["benign_cases"])

    print("Aggregate")
    print(
        "  adversarial_accuracy="
        f"{sum(r['correct'] for r in adversarial_rows) / n_adv:.4f}"
    )
    print(
        "  attack_success_rate="
        f"{sum(r['attack_success'] for r in adversarial_rows) / n_adv:.4f}"
    )
    print(
        "  attack_span_removal_rate="
        f"{sum(r['attack_text_removed'] for r in adversarial_rows) / n_adv:.4f}"
    )
    print(
        "  benign_required_fact_preservation_rate="
        f"{benign_preserved / n_benign:.4f}"
    )


if __name__ == "__main__":
    main()
