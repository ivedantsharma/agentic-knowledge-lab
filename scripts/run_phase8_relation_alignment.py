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
from knowledgebench.evaluation.agent_grounding_grader import (
    grade_agent_grounding,
)
from knowledgebench.evaluation.relation_alignment_grader import (
    grade_relation_alignment,
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
        max_reasonable_search_steps=len(task.hops),
    )


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

        stopped = 0
        grounded = 0
        relation_aligned = 0
        grounded_wrong_relation = 0

        for task in tasks:
            run = execute_with_trace(
                task=task,
                next_action=planner_fn,
                search_tool=search_tool,
                document_by_id=document_by_id,
            )
            eval_task = to_agent_eval_task(task)

            grounding = grade_agent_grounding(
                task=eval_task,
                run=run,
                document_text_by_id=document_text_by_id,
            )
            relation = grade_relation_alignment(
                task=task,
                run=run,
                document_text_by_id=document_text_by_id,
            )

            stopped += relation.stopped
            grounded += grounding.answer_grounded
            relation_aligned += relation.relation_aligned
            grounded_wrong_relation += (
                grounding.answer_grounded
                and not relation.relation_aligned
            )

            print(task.task_id)
            print(
                f"  answer_correct={grounding.answer_correct}"
            )
            print(
                f"  answer_grounded={grounding.answer_grounded}"
            )
            print(
                "  final_evidence_consumed="
                f"{relation.final_evidence_consumed}"
            )
            print(
                "  extracted_relation_answer="
                f"{relation.extracted_relation_answer!r}"
            )
            print(
                f"  relation_aligned={relation.relation_aligned}"
            )
            print(
                "  grounded_wrong_relation="
                f"{grounding.answer_grounded and not relation.relation_aligned}"
            )
            print()

        print("Aggregate")
        print(f"  stopped_count={stopped}")
        print(
            "  grounded_stop_rate="
            f"{grounded / stopped:.4f}"
            if stopped
            else "  grounded_stop_rate=0.0000"
        )
        print(
            "  relation_aligned_stop_rate="
            f"{relation_aligned / stopped:.4f}"
            if stopped
            else "  relation_aligned_stop_rate=0.0000"
        )
        print(
            "  grounded_wrong_relation_rate="
            f"{grounded_wrong_relation / stopped:.4f}"
            if stopped
            else "  grounded_wrong_relation_rate=0.0000"
        )
        print()


if __name__ == "__main__":
    main()
