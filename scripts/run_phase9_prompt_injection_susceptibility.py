import json
from pathlib import Path

from knowledge_engine.agent.qwen_continuation_planner import (
    QwenContinuationPlanner,
)
from knowledgebench.evaluation.prompt_injection_grader import (
    grade_prompt_injection_pair,
)


CASES_PATH = Path(
    "data/processed/phase9_prompt_injection_pairs_v0.json"
)


def main() -> None:
    payload = json.loads(
        CASES_PATH.read_text(
            encoding="utf-8"
        )
    )
    model_name = payload["model"]

    planner = QwenContinuationPlanner(
        model_name=model_name,
        relation_verifier=None,
    )

    grades = []

    print(
        "Phase 9 EXP-083 — Retrieved-Content "
        "Prompt-Injection Susceptibility"
    )
    print(f"model={model_name}")
    print()

    for case in payload["cases"]:
        clean_candidate = (
            planner.extract_or_abstain(
                case["question"],
                case["clean_evidence"],
            )
        )
        injected_candidate = (
            planner.extract_or_abstain(
                case["question"],
                case["injected_evidence"],
            )
        )

        grade = grade_prompt_injection_pair(
            case_id=case["case_id"],
            clean_candidate=clean_candidate,
            injected_candidate=(
                injected_candidate
            ),
            expected_answer=case[
                "expected_answer"
            ],
            attack_payload=case[
                "attack_payload"
            ],
        )
        grades.append(grade)

        print(case["case_id"])
        print(
            "  clean_candidate="
            f"{clean_candidate!r}"
        )
        print(
            "  injected_candidate="
            f"{injected_candidate!r}"
        )
        print(
            "  expected_answer="
            f"{case['expected_answer']!r}"
        )
        print(
            "  attack_payload="
            f"{case['attack_payload']!r}"
        )
        print(
            f"  clean_correct={grade.clean_correct}"
        )
        print(
            "  injected_correct="
            f"{grade.injected_correct}"
        )
        print(
            f"  attack_success={grade.attack_success}"
        )
        print(
            "  behavior_changed="
            f"{grade.behavior_changed}"
        )
        print()

    cases = len(grades)
    clean_accuracy = (
        sum(g.clean_correct for g in grades)
        / cases
    )
    injected_accuracy = (
        sum(g.injected_correct for g in grades)
        / cases
    )
    attack_success_rate = (
        sum(g.attack_success for g in grades)
        / cases
    )
    behavior_change_rate = (
        sum(g.behavior_changed for g in grades)
        / cases
    )

    print("Aggregate")
    print(
        f"  clean_accuracy={clean_accuracy:.4f}"
    )
    print(
        "  injected_accuracy="
        f"{injected_accuracy:.4f}"
    )
    print(
        "  attack_success_rate="
        f"{attack_success_rate:.4f}"
    )
    print(
        "  behavior_change_rate="
        f"{behavior_change_rate:.4f}"
    )


if __name__ == "__main__":
    main()
