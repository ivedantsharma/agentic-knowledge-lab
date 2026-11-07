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
from knowledge_engine.agent.state import (
    PlannerState,
    PlannerTraceStep,
)
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CORPUS_PATH = Path(
    "data/processed/phase3_multihop_corpus_v3.jsonl"
)
TASK_PATH = Path(
    "data/processed/phase3_multihop_tasks_v4.json"
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

    correct_answers = 0
    stopped_tasks = 0

    for task in tasks:
        state = PlannerState(
            question=task.question
        )

        print(task.task_id)
        print(f"question={task.question}")
        print()

        while (
            not state.stopped
            and state.step_index < MAX_STEPS
        ):
            action = planner.next_action(state)

            print(
                f"step={state.step_index} "
                f"action={action.action_type}"
            )

            if action.action_type == PlannerActionType.STOP:
                state.final_answer = action.answer
                state.stopped = True
                stopped_tasks += 1

                state.trace.append(
                    PlannerTraceStep(
                        step_index=state.step_index,
                        action_type=action.action_type,
                        metadata={
                            "answer": action.answer,
                        },
                    )
                )

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

            retrieved_id, score = ranking[0]
            retrieved_document = document_by_id[
                retrieved_id
            ]

            new_retrieval_state = (
                parse_retrieval_observation(
                    retrieved_id,
                    retrieved_document.text,
                )
            )

            state.trace.append(
                PlannerTraceStep(
                    step_index=state.step_index,
                    action_type=action.action_type,
                    query=action.query,
                    retrieved_document_id=retrieved_id,
                    extracted_fact=(
                        new_retrieval_state.entity
                    ),
                    metadata={
                        "top3": ranking,
                        "score": score,
                        "qualifiers": (
                            new_retrieval_state.qualifiers
                        ),
                    },
                )
            )

            state.retrieval_state = (
                new_retrieval_state
            )

            print(f"  query={action.query}")
            print(f"  top3={ranking}")
            print(f"  retrieved={retrieved_id}")
            print(
                "  state="
                f"{state.retrieval_state.model_dump()}"
            )
            print()

            state.step_index += 1

        if not state.stopped:
            print(
                f"Stopped by MAX_STEPS={MAX_STEPS} safeguard"
            )

        answer_correct = (
            state.final_answer is not None
            and state.final_answer.casefold()
            == task.expected_answer.casefold()
        )

        correct_answers += int(answer_correct)

        print(
            f"trace_steps={len(state.trace)}"
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
        "StoppedRate="
        f"{stopped_tasks / len(tasks):.4f}"
    )
    print(
        "AnswerAccuracy="
        f"{correct_answers / len(tasks):.4f}"
    )


if __name__ == "__main__":
    main()
