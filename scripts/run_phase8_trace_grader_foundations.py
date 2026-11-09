import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledgebench.evaluation.agent_trace_grader import (
    grade_agent_trace,
)
from knowledgebench.runs.agent_trace_schema import (
    AgentRunTrace,
)
from knowledgebench.tasks.agent_eval_schema import (
    AgentEvalTask,
)

CASES_PATH = Path(
    "data/processed/phase8_agent_trace_cases_v0.json"
)


def main() -> None:
    payload = json.loads(
        CASES_PATH.read_text(
            encoding="utf-8"
        )
    )

    tasks = {
        task.task_id: task
        for task in (
            AgentEvalTask.model_validate(item)
            for item in payload["tasks"]
        )
    }

    print("Phase 8 EXP-075 — Deterministic Trace Graders")

    for raw_run in payload["runs"]:
        case_name = raw_run["case_name"]
        run_payload = {
            key: value
            for key, value in raw_run.items()
            if key != "case_name"
        }
        run = AgentRunTrace.model_validate(
            run_payload
        )
        grade = grade_agent_trace(
            tasks[run.task_id],
            run,
        )

        print(case_name)
        print(
            f"  search_steps={grade.search_steps}"
        )
        print(
            f"  repeated_searches={grade.repeated_searches}"
        )
        print(
            "  required_evidence_coverage="
            f"{grade.required_evidence_coverage:.4f}"
        )
        print(
            f"  stopped={grade.stopped}"
        )
        print(
            f"  answer_correct={grade.answer_correct}"
        )
        print(
            f"  premature_stop={grade.premature_stop}"
        )
        print(
            f"  efficient_search={grade.efficient_search}"
        )
        print(
            "  retrieved_required_evidence="
            f"{grade.retrieved_required_evidence}"
        )
        print()


if __name__ == "__main__":
    main()
