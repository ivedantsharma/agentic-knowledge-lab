import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import knowledge_engine.agent.qwen_continuation_planner as qwen_planner_module
from knowledge_engine.agent.actions import PlannerActionType
from knowledge_engine.agent.observation_parser import (
    parse_retrieval_observation,
)
from knowledge_engine.agent.qwen_continuation_planner import (
    PLANNER_IMPLEMENTATION_VERSION,
    QwenContinuationPlanner,
)
from knowledge_engine.agent.search_tool import DenseSearchTool
from knowledge_engine.agent.semantic_planner import SemanticPlanner
from knowledge_engine.agent.state import PlannerState
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
QWEN_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

CORPUS_PATH = Path(
    "data/processed/phase4_ood_corpus_v0.jsonl"
)
TASK_PATH = Path(
    "data/processed/phase4_ood_tasks_v0.json"
)

MAX_STEPS = 6


def main() -> None:
    documents = load_documents_jsonl(CORPUS_PATH)
    tasks = load_multihop_tasks_json(TASK_PATH)

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

    bootstrap_planner = SemanticPlanner(
        documents=documents,
        model_name=EMBEDDING_MODEL,
        model=embedding_model,
    )

    continuation_planner = QwenContinuationPlanner(
        model_name=QWEN_MODEL,
    )

    print(
        "qwen_planner_module="
        f"{qwen_planner_module.__file__}"
    )
    print(
        "qwen_planner_version="
        f"{PLANNER_IMPLEMENTATION_VERSION}"
    )
    print()

    for task in tasks:
        state = PlannerState(
            question=task.question
        )

        print(task.task_id)
        print(f"question={task.question}")
        print()

        planner_failed = False

        while (
            not state.stopped
            and state.step_index < MAX_STEPS
        ):
            try:
                if state.step_index == 0:
                    action = bootstrap_planner.next_action(
                        state
                    )
                    planner_name = "semantic_bootstrap"
                else:
                    decision = (
                        continuation_planner.inspect_decision(
                            state
                        )
                    )
                    print(
                        "  answerable="
                        f"{decision['answerable']}"
                    )
                    print(
                        "  candidate_answer="
                        f"{decision['candidate_answer']!r}"
                    )
                    print(
                        "  abstained="
                        f"{decision['abstained']}"
                    )
                    print(
                        "  grounded="
                        f"{decision['grounded']}"
                    )

                    action = continuation_planner.next_action(
                        state
                    )
                    planner_name = "qwen_continuation"
            except ValueError as error:
                planner_failed = True
                print(f"planner_error={error}")
                break

            print(
                f"step={state.step_index} "
                f"planner={planner_name} "
                f"action={action.action_type}"
            )

            if action.action_type == PlannerActionType.STOP:
                state.final_answer = action.answer
                state.stopped = True
                print(f"  answer={action.answer}")
                break

            if action.query is None:
                raise ValueError(
                    "SEARCH action missing query"
                )

            ranking = search_tool.search(
                action.query,
                top_k=3,
            )

            retrieved_id, _score = ranking[0]
            retrieved_document = document_by_id[
                retrieved_id
            ]

            state.retrieval_state = (
                parse_retrieval_observation(
                    retrieved_id,
                    retrieved_document.text,
                )
            )

            print(f"  query={action.query}")
            print(f"  top3={ranking}")
            print(f"  retrieved={retrieved_id}")
            print(
                f"  state={state.retrieval_state.model_dump()}"
            )
            print()

            state.step_index += 1

        if not state.stopped and not planner_failed:
            print(
                f"Stopped by MAX_STEPS={MAX_STEPS} safeguard"
            )

        answer_correct = (
            state.final_answer is not None
            and "cirrus-dlq"
            in state.final_answer.casefold()
        )

        print(f"planner_failed={planner_failed}")
        print(f"final_answer={state.final_answer}")
        print(f"expected_answer={task.expected_answer}")
        print(
            "AnswerCorrect="
            f"{float(answer_correct):.4f}"
        )


if __name__ == "__main__":
    main()
