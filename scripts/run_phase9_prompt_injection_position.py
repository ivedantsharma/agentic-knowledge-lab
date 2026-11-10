import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.qwen_continuation_planner import (
    QwenContinuationPlanner,
)
from knowledgebench.evaluation.short_answer_equivalence import (
    short_answers_equivalent,
)


CASES_PATH = Path(
    "data/processed/phase9_prompt_injection_position_v0.json"
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

    rows = []
    by_variant: dict[str, list[dict]] = defaultdict(list)

    print(
        "Phase 9 EXP-085 — Prompt-Injection "
        "Placement and Framing Sensitivity"
    )
    print(f"model={payload['model']}")
    print()

    for case in payload["cases"]:
        candidate = planner.extract_or_abstain(
            case["question"],
            case["evidence"],
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

        row = {
            "variant": case["variant"],
            "correct": correct,
            "attack_success": attack_success,
        }
        rows.append(row)
        by_variant[case["variant"]].append(row)

        print(case["case_id"])
        print(f"  family={case['family']}")
        print(f"  variant={case['variant']}")
        print(f"  candidate={candidate!r}")
        print(f"  correct={correct}")
        print(
            f"  attack_success={attack_success}"
        )
        print()

    print("By variant")
    for variant, variant_rows in by_variant.items():
        n = len(variant_rows)
        print(variant)
        print(
            "  accuracy="
            f"{sum(r['correct'] for r in variant_rows) / n:.4f}"
        )
        print(
            "  attack_success_rate="
            f"{sum(r['attack_success'] for r in variant_rows) / n:.4f}"
        )

    print()
    print("Aggregate")
    n = len(rows)
    print(
        "  accuracy="
        f"{sum(r['correct'] for r in rows) / n:.4f}"
    )
    print(
        "  attack_success_rate="
        f"{sum(r['attack_success'] for r in rows) / n:.4f}"
    )


if __name__ == "__main__":
    main()
