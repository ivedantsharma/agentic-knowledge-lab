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
from knowledge_engine.agent.state import (
    PlannerState,
)
from knowledgebench.documents.loader import (
    load_documents_jsonl,
)
from knowledgebench.evaluation.agent_grounding_grader import (
    grade_agent_grounding,
)
from knowledgebench.evaluation.agent_trace_grader import (
    grade_agent_trace,
)
from knowledgebench.runs.agent_trace_schema import (
    AgentRunTrace,
    AgentTraceStep,
)
from knowledgebench.tasks.agent_eval_schema import (
    AgentEvalTask,
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


def to_agent_eval_task(
    task: MultiHopTask,
) -> AgentEvalTask:
    return AgentEvalTask(
        task_id=task.task_id,
        question=task.question,
        expected_answer=task.expected_answer,
        required_document_ids=[
            hop.expected_document_id
            for hop in task.hops
        ],
        max_reasonable_search_steps=len(
            task.hops
        ),
    )


def execute_with_trace(
    *,
    task: MultiHopTask,
    next_action: Callable[
        [PlannerState],
        PlannerAction,
    ],
    search_tool: DenseSearchTool,
    document_by_id: dict,
) -> AgentRunTrace:
    state = PlannerState(
        question=task.question
    )
    trace_steps: list[AgentTraceStep] = []

    while (
        not state.stopped
        and state.step_index < MAX_STEPS
    ):
        try:
            action = next_action(state)
        except ValueError as error:
            return AgentRunTrace(
                task_id=task.task_id,
                steps=trace_steps,
                metadata={
                    "planner_failed": True,
                    "planner_error": str(error),
                },
            )

        if action.action_type == PlannerActionType.STOP:
            trace_steps.append(
                AgentTraceStep(
                    step_index=len(trace_steps),
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

        trace_steps.append(
            AgentTraceStep(
                step_index=len(trace_steps),
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
        steps=trace_steps,
        metadata={
            "planner_failed": False,
            "max_steps_exhausted": (
                not state.stopped
                and state.step_index >= MAX_STEPS
            ),
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
    document_text_by_id = {
        document.document_id: document.text
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

        grounded_count = 0
        grounded_wrong_count = 0
        stopped_count = 0

        for task in tasks:
            run = execute_with_trace(
                task=task,
                next_action=planner_fn,
                search_tool=search_tool,
                document_by_id=document_by_id,
            )
            eval_task = to_agent_eval_task(
                task
            )
            trace_grade = grade_agent_trace(
                eval_task,
                run,
            )
            grounding_grade = grade_agent_grounding(
                task=eval_task,
                run=run,
                document_text_by_id=(
                    document_text_by_id
                ),
            )

            stopped_count += grounding_grade.stopped
            grounded_count += (
                grounding_grade.answer_grounded
            )
            grounded_wrong_count += (
                grounding_grade.grounded_but_wrong
            )

            print(task.task_id)
            print(
                "  evidence_coverage="
                f"{trace_grade.required_evidence_coverage:.4f}"
            )
            print(
                "  answer_correct="
                f"{grounding_grade.answer_correct}"
            )
            print(
                "  answer_grounded="
                f"{grounding_grade.answer_grounded}"
            )
            print(
                "  grounded_but_wrong="
                f"{grounding_grade.grounded_but_wrong}"
            )
            print(
                "  grounding_documents="
                f"{grounding_grade.supporting_document_ids}"
            )
            print()

        print("Aggregate")
        print(
            "  stopped_count="
            f"{stopped_count}"
        )
        print(
            "  grounded_stop_rate="
            f"{grounded_count / stopped_count:.4f}"
            if stopped_count
            else "  grounded_stop_rate=0.0000"
        )
        print(
            "  grounded_but_wrong_rate="
            f"{grounded_wrong_count / stopped_count:.4f}"
            if stopped_count
            else "  grounded_but_wrong_rate=0.0000"
        )
        print()


if __name__ == "__main__":
    main()
