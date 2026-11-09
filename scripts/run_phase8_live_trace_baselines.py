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
from knowledgebench.evaluation.agent_trace_grader import (
    aggregate_agent_trace_grades,
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
        metadata={
            "source": "phase4_planner_benchmark_v0",
            "category": task.category,
        },
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
            state.final_answer = action.answer
            state.stopped = True
            break

        if action.query is None:
            return AgentRunTrace(
                task_id=task.task_id,
                steps=trace_steps,
                metadata={
                    "planner_failed": True,
                    "planner_error": (
                        "SEARCH action missing query"
                    ),
                },
            )

        ranking = search_tool.search(
            action.query,
            top_k=3,
        )
        retrieved_id, score = ranking[0]
        retrieved_document = document_by_id[
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
                retrieved_document.text,
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


def print_planner_result(
    planner_name: str,
    tasks: list[MultiHopTask],
    runs: list[AgentRunTrace],
) -> None:
    eval_tasks = {
        task.task_id: to_agent_eval_task(task)
        for task in tasks
    }
    grades = [
        grade_agent_trace(
            eval_tasks[run.task_id],
            run,
        )
        for run in runs
    ]

    print(f"=== {planner_name} ===")

    for run, grade in zip(runs, grades):
        print(run.task_id)
        print(
            "  actions="
            f"{[step.action_type.value for step in run.steps]}"
        )
        print(
            "  queries="
            f"{[step.query for step in run.steps if step.query is not None]}"
        )
        print(
            "  retrieved="
            f"{[doc for step in run.steps for doc in step.retrieved_document_ids]}"
        )
        print(
            f"  search_steps={grade.search_steps}"
        )
        print(
            "  evidence_coverage="
            f"{grade.required_evidence_coverage:.4f}"
        )
        print(
            f"  answer_correct={grade.answer_correct}"
        )
        print(
            f"  premature_stop={grade.premature_stop}"
        )
        print(
            f"  repeated_searches={grade.repeated_searches}"
        )
        print(
            f"  efficient_search={grade.efficient_search}"
        )
        print(
            f"  metadata={run.metadata}"
        )
        print()

    aggregate = aggregate_agent_trace_grades(
        grades
    )

    print("Aggregate")
    print(f"  tasks={aggregate.tasks}")
    print(
        "  answer_accuracy="
        f"{aggregate.answer_accuracy:.4f}"
    )
    print(
        "  full_evidence_rate="
        f"{aggregate.full_evidence_rate:.4f}"
    )
    print(
        "  premature_stop_rate="
        f"{aggregate.premature_stop_rate:.4f}"
    )
    print(
        "  efficient_search_rate="
        f"{aggregate.efficient_search_rate:.4f}"
    )
    print(
        "  average_search_steps="
        f"{aggregate.average_search_steps:.4f}"
    )
    print(
        "  average_repeated_searches="
        f"{aggregate.average_repeated_searches:.4f}"
    )
    print()


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
        runs = [
            execute_with_trace(
                task=task,
                next_action=planner_fn,
                search_tool=search_tool,
                document_by_id=document_by_id,
            )
            for task in tasks
        ]
        print_planner_result(
            planner_name,
            tasks,
            runs,
        )


if __name__ == "__main__":
    main()
