import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.agent.actions import PlannerActionType
from knowledge_engine.agent.oracle_planner import OraclePlanner
from knowledge_engine.agent.search_tool import DenseSearchTool
from knowledge_engine.agent.state import (
    PlannerState,
    PlannerTraceStep,
)
from knowledge_engine.retrieval.fact_extractor import (
    extract_fact,
)
from knowledge_engine.retrieval.state import RetrievalState
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
    planner = OraclePlanner()

    correct_answers = 0

    for task in tasks:
        state = PlannerState(
            question=task.question
        )

        print(task.task_id)
        print(f"question={task.question}")
        print()

        while not state.stopped:
            action = planner.next_action(
                task,
                state,
            )

            print(
                f"step={state.step_index} "
                f"action={action.action_type}"
            )

            if action.action_type == PlannerActionType.STOP:
                state.final_answer = action.answer
                state.stopped = True

                state.trace.append(
                    PlannerTraceStep(
                        step_index=state.step_index,
                        action_type=action.action_type,
                        metadata={
                            "answer": action.answer,
                        },
                    )
                )

                print(
                    f"  answer={action.answer}"
                )
                break

            if action.query is None:
                raise ValueError(
                    "SEARCH action missing query"
                )

            hop = task.hops[state.step_index]

            ranking = search_tool.search(
                action.query,
                top_k=3,
            )
            retrieved_id, score = ranking[0]
            retrieved_document = document_by_id[
                retrieved_id
            ]

            if hop.extraction_pattern is None:
                raise ValueError(
                    "oracle executor requires "
                    "extraction_pattern"
                )

            extracted_fact = extract_fact(
                retrieved_document.text,
                hop.extraction_pattern,
            )

            extracted_qualifier = None
            if hop.qualifier_pattern is not None:
                extracted_qualifier = extract_fact(
                    retrieved_document.text,
                    hop.qualifier_pattern,
                )

            state.trace.append(
                PlannerTraceStep(
                    step_index=state.step_index,
                    action_type=action.action_type,
                    query=action.query,
                    retrieved_document_id=retrieved_id,
                    extracted_fact=extracted_fact,
                    metadata={
                        "top3": ranking,
                        "score": score,
                        "qualifier": extracted_qualifier,
                    },
                )
            )

            state.retrieval_state = RetrievalState(
                entity=extracted_fact,
                qualifiers=(
                    [extracted_qualifier]
                    if extracted_qualifier is not None
                    else []
                ),
                source_document_id=retrieved_id,
                evidence_text=retrieved_document.text,
            )

            print(f"  query={action.query}")
            print(f"  top3={ranking}")
            print(
                f"  retrieved={retrieved_id}"
            )
            print(
                f"  extracted_fact={extracted_fact}"
            )
            print(
                f"  qualifier={extracted_qualifier}"
            )
            print(
                "  retrieval_state="
                f"{state.retrieval_state.model_dump()}"
            )
            print()

            state.step_index += 1

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
        "AnswerAccuracy="
        f"{correct_answers / len(tasks):.4f}"
    )


if __name__ == "__main__":
    main()
