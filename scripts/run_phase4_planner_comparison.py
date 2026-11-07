import sys
from pathlib import Path
from typing import Callable

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.actions import PlannerAction, PlannerActionType
from knowledge_engine.agent.evaluation import (
    PlannerTaskResult,
    aggregate_planner_results,
)
from knowledge_engine.agent.observation_parser import (
    parse_retrieval_observation,
)
from knowledge_engine.agent.qwen_continuation_planner import (
    QwenContinuationPlanner,
)
from knowledge_engine.agent.qwen_relation_verifier import (
    QwenRelationVerifier,
)
from knowledge_engine.agent.rule_based_planner import RuleBasedPlanner
from knowledge_engine.agent.search_tool import DenseSearchTool
from knowledge_engine.agent.semantic_planner import SemanticPlanner
from knowledge_engine.agent.state import PlannerState
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
QWEN_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
QWEN_VERIFIER_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

CORPUS_PATH = Path(
    "data/processed/phase4_ood_corpus_v0.jsonl"
)
TASK_PATH = Path(
    "data/processed/phase4_planner_benchmark_v0.json"
)

MAX_STEPS = 6


def execute_task(
    *,
    task,
    planner_name: str,
    next_action: Callable[[PlannerState], PlannerAction],
    search_tool: DenseSearchTool,
    document_by_id: dict,
) -> PlannerTaskResult:
    state = PlannerState(
        question=task.question
    )
    retrieved_document_ids: list[str] = []
    search_steps = 0
    planner_failed = False

    print(task.task_id)
    print(f"question={task.question}")

    while (
        not state.stopped
        and state.step_index < MAX_STEPS
    ):
        try:
            action = next_action(state)
        except ValueError as error:
            planner_failed = True
            print(f"  planner_error={error}")
            break

        print(
            f"  step={state.step_index} "
            f"action={action.action_type}"
        )

        if action.action_type == PlannerActionType.STOP:
            state.final_answer = action.answer
            state.stopped = True
            print(f"    answer={action.answer}")
            break

        if action.query is None:
            planner_failed = True
            print("  planner_error=SEARCH action missing query")
            break

        ranking = search_tool.search(
            action.query,
            top_k=3,
        )

        retrieved_id, _score = ranking[0]
        retrieved_document = document_by_id[
            retrieved_id
        ]

        retrieved_document_ids.append(
            retrieved_id
        )
        search_steps += 1

        state.retrieval_state = (
            parse_retrieval_observation(
                retrieved_id,
                retrieved_document.text,
            )
        )

        print(f"    query={action.query}")
        print(f"    retrieved={retrieved_id}")
        print(f"    top3={ranking}")

        state.step_index += 1

    max_steps_exhausted = (
        not state.stopped
        and not planner_failed
        and state.step_index >= MAX_STEPS
    )

    result = PlannerTaskResult(
        task_id=task.task_id,
        expected_answer=task.expected_answer,
        final_answer=state.final_answer,
        stopped=state.stopped,
        planner_failed=planner_failed,
        max_steps_exhausted=max_steps_exhausted,
        search_steps=search_steps,
        retrieved_document_ids=retrieved_document_ids,
        final_evidence_document_id=(
            task.hops[-1].expected_document_id
        ),
    )

    print(f"  stopped={result.stopped}")
    print(f"  answer_correct={result.answer_correct}")
    print(
        "  final_evidence_retrieved="
        f"{result.final_evidence_retrieved}"
    )
    print(
        f"  premature_stop={result.premature_stop}"
    )
    print(
        f"  planner_failed={result.planner_failed}"
    )
    print()

    return result


def print_metrics(
    planner_name: str,
    results: list[PlannerTaskResult],
) -> None:
    metrics = aggregate_planner_results(
        results
    )

    print(f"=== {planner_name} Aggregate ===")
    print(f"Tasks={metrics.tasks}")
    print(
        f"AnswerAccuracy={metrics.answer_accuracy:.4f}"
    )
    print(
        "PlannerFailureRate="
        f"{metrics.planner_failure_rate:.4f}"
    )
    print(
        f"StoppedRate={metrics.stopped_rate:.4f}"
    )
    print(
        f"StopPrecision={metrics.stop_precision:.4f}"
    )
    print(
        "PrematureStopRate="
        f"{metrics.premature_stop_rate:.4f}"
    )
    print(
        "SearchSuccessRate="
        f"{metrics.search_success_rate:.4f}"
    )
    print(
        "AverageSearchSteps="
        f"{metrics.average_search_steps:.4f}"
    )
    print(
        "MaxStepExhaustionRate="
        f"{metrics.max_step_exhaustion_rate:.4f}"
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

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    search_tool = DenseSearchTool(
        documents=documents,
        model_name=EMBEDDING_MODEL,
        model=embedding_model,
    )

    semantic_planner = SemanticPlanner(
        documents=documents,
        model_name=EMBEDDING_MODEL,
        model=embedding_model,
    )

    rule_planner = RuleBasedPlanner()

    relation_verifier = QwenRelationVerifier(
        model_name=QWEN_VERIFIER_MODEL,
    )

    continuation_planner = QwenContinuationPlanner(
        model_name=QWEN_MODEL,
        relation_verifier=relation_verifier,
    )

    planners: list[
        tuple[
            str,
            Callable[[PlannerState], PlannerAction],
        ]
    ] = [
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
        print(
            f"\n######## {planner_name} ########\n"
        )
        results = [
            execute_task(
                task=task,
                planner_name=planner_name,
                next_action=planner_fn,
                search_tool=search_tool,
                document_by_id=document_by_id,
            )
            for task in tasks
        ]
        print_metrics(
            planner_name,
            results,
        )

    def hybrid_next_action(
        state: PlannerState,
    ) -> PlannerAction:
        if state.step_index == 0:
            return semantic_planner.next_action(
                state
            )

        decision = (
            continuation_planner.inspect_decision(
                state
            )
        )

        print(
            "    candidate_answer="
            f"{decision['candidate_answer']!r}"
        )
        print(
            "    grounded="
            f"{decision['grounded']}"
        )
        print(
            "    relation_aligned="
            f"{decision['relation_aligned']}"
        )

        return (
            continuation_planner.action_from_decision(
                state,
                decision,
            )
        )

    print(
        "\n######## hybrid ########\n"
    )
    hybrid_results = [
        execute_task(
            task=task,
            planner_name="hybrid",
            next_action=hybrid_next_action,
            search_tool=search_tool,
            document_by_id=document_by_id,
        )
        for task in tasks
    ]
    print_metrics(
        "hybrid",
        hybrid_results,
    )


if __name__ == "__main__":
    main()
