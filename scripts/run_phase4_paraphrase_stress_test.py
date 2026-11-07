import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.actions import PlannerActionType
from knowledge_engine.agent.observation_parser import (
    parse_retrieval_observation,
)
from knowledge_engine.agent.rule_based_planner import (
    RuleBasedPlanner,
)
from knowledge_engine.agent.search_tool import DenseSearchTool
from knowledge_engine.agent.state import PlannerState
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CORPUS_PATH = Path(
    "data/processed/phase3_multihop_corpus_v3.jsonl"
)
TASK_PATH = Path(
    "data/processed/phase4_paraphrase_tasks_v0.json"
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
        model_name=MODEL_NAME,
    )
    planner = RuleBasedPlanner()

    planned_tasks = 0
    stopped_tasks = 0
    correct_answers = 0

    for task in tasks:
        state = PlannerState(
            question=task.question
        )

        print(task.task_id)
        print(f"question={task.question}")

        planner_failed = False

        while (
            not state.stopped
            and state.step_index < MAX_STEPS
        ):
            try:
                action = planner.next_action(state)
            except ValueError as error:
                planner_failed = True
                print(
                    f"planner_error={error}"
                )
                break

            if state.step_index == 0:
                planned_tasks += 1

            print(
                f"step={state.step_index} "
                f"action={action.action_type}"
            )

            if action.action_type == PlannerActionType.STOP:
                state.final_answer = action.answer
                state.stopped = True
                stopped_tasks += 1
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

        answer_correct = (
            state.final_answer is not None
            and state.final_answer.casefold()
            == task.expected_answer.casefold()
        )

        correct_answers += int(answer_correct)

        print(
            f"planner_failed={planner_failed}"
        )
        print(
            f"final_answer={state.final_answer}"
        )
        print(
            f"expected_answer={task.expected_answer}"
        )
        print(
            "AnswerCorrect="
            f"{float(answer_correct):.4f}"
        )
        print()

    print("Aggregate")
    print(f"tasks={len(tasks)}")
    print(
        "InitialPlanRate="
        f"{planned_tasks / len(tasks):.4f}"
    )
    print(
        "StoppedRate="
        f"{stopped_tasks / len(tasks):.4f}"
    )
    print(
        "AnswerAccuracy="
        f"{correct_answers / len(tasks):.4f}"
    )


if __name__ == "__main__":
    main()
