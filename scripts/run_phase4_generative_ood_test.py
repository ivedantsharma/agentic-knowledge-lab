import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.actions import PlannerActionType
from knowledge_engine.agent.generative_planner import (
    LocalGenerativePlanner,
)
from knowledge_engine.agent.observation_parser import (
    parse_retrieval_observation,
)
from knowledge_engine.agent.search_tool import DenseSearchTool
from knowledge_engine.agent.state import PlannerState
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PLANNER_MODEL = "google/flan-t5-small"

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

    search_tool = DenseSearchTool(
        documents=documents,
        model_name=EMBEDDING_MODEL,
    )

    planner = LocalGenerativePlanner(
        model_name=PLANNER_MODEL,
    )

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
                action = planner.next_action(state)
            except ValueError as error:
                planner_failed = True
                print(f"planner_error={error}")
                break

            print(
                f"step={state.step_index} "
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

            state.step_index += 1

        if not state.stopped and not planner_failed:
            print(
                f"Stopped by MAX_STEPS={MAX_STEPS} safeguard"
            )

        answer_correct = (
            state.final_answer is not None
            and state.final_answer.casefold()
            == task.expected_answer.casefold()
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
