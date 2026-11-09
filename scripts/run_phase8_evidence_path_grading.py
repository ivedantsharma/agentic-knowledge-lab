from collections.abc import Callable
from pathlib import Path

from sentence_transformers import SentenceTransformer

from knowledge_engine.agent.actions import (
    PlannerAction,
    PlannerActionType,
)
from knowledge_engine.agent.observation_parser import (
    parse_retrieval_observation,
)
from knowledge_engine.agent.rule_based_planner import (
    RuleBasedPlanner,
)
from knowledge_engine.agent.search_tool import (
    DenseSearchTool,
)
from knowledge_engine.agent.semantic_planner import (
    SemanticPlanner,
)
from knowledge_engine.agent.state import PlannerState
from knowledgebench.documents.loader import (
    load_documents_jsonl,
)
from knowledgebench.evaluation.evidence_path_grader import (
    grade_evidence_path,
)
from knowledgebench.runs.agent_trace_schema import (
    AgentRunTrace,
    AgentTraceStep,
)
from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)
from knowledgebench.tasks.multihop_schema import (
    MultiHopTask,
)


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CORPUS_PATH = Path(
    "data/processed/phase4_ood_corpus_v0.jsonl"
)
TASK_PATH = Path(
    "data/processed/phase4_planner_benchmark_v0.json"
)
MAX_STEPS = 6


def execute_with_trace(
    *,
    task: MultiHopTask,
    next_action: Callable[[PlannerState], PlannerAction],
    search_tool: DenseSearchTool,
    document_by_id: dict,
) -> AgentRunTrace:
    state = PlannerState(
        question=task.question
    )
    steps: list[AgentTraceStep] = []

    while (
        not state.stopped
        and state.step_index < MAX_STEPS
    ):
        try:
            action = next_action(state)
        except ValueError as error:
            return AgentRunTrace(
                task_id=task.task_id,
                steps=steps,
                metadata={
                    "planner_failed": True,
                    "planner_error": str(error),
                },
            )

        if action.action_type == PlannerActionType.STOP:
            steps.append(
                AgentTraceStep(
                    step_index=len(steps),
                    action_type="stop",
                    answer=action.answer,
                )
            )
            state.stopped = True
            break

        ranking = search_tool.search(
            action.query or "",
            top_k=3,
        )
        retrieved_id, score = ranking[0]
        document = document_by_id[
            retrieved_id
        ]

        steps.append(
            AgentTraceStep(
                step_index=len(steps),
                action_type="search",
                query=action.query,
                retrieved_document_ids=[
                    retrieved_id
                ],
                metadata={
                    "top1_score": score,
                },
            )
        )

        state.retrieval_state = (
            parse_retrieval_observation(
                retrieved_id,
                document.text,
            )
        )
        state.step_index += 1

    return AgentRunTrace(
        task_id=task.task_id,
        steps=steps,
        metadata={
            "planner_failed": False,
        },
    )


def main() -> None:
    documents = load_documents_jsonl(
        CORPUS_PATH
    )
    tasks = load_multihop_tasks_json(
        TASK_PATH
    )
    document_by_id = {
        document.document_id: document
        for document in documents
    }

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )
    search_tool = DenseSearchTool(
        documents=documents,
        model_name=EMBEDDING_MODEL,
        model=model,
    )

    rule_planner = RuleBasedPlanner()
    semantic_planner = SemanticPlanner(
        documents=documents,
        model_name=EMBEDDING_MODEL,
        model=model,
    )

    planners = [
        (
            "rule_based",
            rule_planner.next_action,
        ),
        (
            "semantic",
            semantic_planner.next_action,
        ),
    ]

    for planner_name, planner_fn in planners:
        print(f"=== {planner_name} ===")

        exact_count = 0
        ordered_count = 0
        coverage_sum = 0.0
        extra_sum = 0

        for task in tasks:
            run = execute_with_trace(
                task=task,
                next_action=planner_fn,
                search_tool=search_tool,
                document_by_id=document_by_id,
            )
            grade = grade_evidence_path(
                task=task,
                run=run,
            )

            exact_count += grade.exact_path_match
            ordered_count += (
                grade.ordered_path_complete
            )
            coverage_sum += grade.path_coverage
            extra_sum += grade.extra_documents

            print(task.task_id)
            print(
                f"  expected_path={grade.expected_path}"
            )
            print(
                f"  consumed_path={grade.consumed_path}"
            )
            print(
                "  path_coverage="
                f"{grade.path_coverage:.4f}"
            )
            print(
                "  ordered_path_complete="
                f"{grade.ordered_path_complete}"
            )
            print(
                "  exact_path_match="
                f"{grade.exact_path_match}"
            )
            print(
                f"  extra_documents={grade.extra_documents}"
            )
            print()

        task_count = len(tasks)

        print("Aggregate")
        print(
            "  mean_path_coverage="
            f"{coverage_sum / task_count:.4f}"
        )
        print(
            "  ordered_path_complete_rate="
            f"{ordered_count / task_count:.4f}"
        )
        print(
            "  exact_path_match_rate="
            f"{exact_count / task_count:.4f}"
        )
        print(
            "  average_extra_documents="
            f"{extra_sum / task_count:.4f}"
        )
        print()


if __name__ == "__main__":
    main()
