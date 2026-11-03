import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.retrieval.fact_extractor import extract_fact
from knowledge_engine.retrieval.state import RetrievalState
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.metrics.multihop import (
    exact_chain_match,
    fact_accuracy,
    hop_accuracy,
)
from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)
from scripts.run_phase3_structured_state_chain import (
    rank_documents,
    render_state_query,
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

    model = SentenceTransformer(MODEL_NAME)

    document_embeddings = model.encode(
        [document.text for document in documents]
    )

    total_hops = 0
    correct_hops = 0
    total_facts = 0
    correct_facts = 0
    exact_chains = 0
    correct_answers = 0

    for task in tasks:
        state = RetrievalState()
        retrieved_chain: list[str] = []
        expected_chain: list[str] = []
        extracted_facts: list[str | None] = []
        expected_facts: list[str] = []

        print(task.task_id)
        print(f"category={task.category}")
        print(f"question={task.question}")
        print()

        for hop in task.hops:
            template = hop.query_template or hop.query
            rendered_query = render_state_query(
                template,
                state,
            )

            ranking = rank_documents(
                rendered_query,
                documents,
                document_embeddings,
                model,
            )
            top3 = ranking[:3]

            retrieved_id, _score = top3[0]
            retrieved_document = document_by_id[
                retrieved_id
            ]

            if hop.extraction_pattern is None:
                raise ValueError(
                    "extraction_pattern is required"
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

            retrieved_chain.append(retrieved_id)
            expected_chain.append(
                hop.expected_document_id
            )
            extracted_facts.append(extracted_fact)
            expected_facts.append(
                hop.expected_fact
            )

            print(f"hop={hop.hop_index + 1}")
            print(f"  query={rendered_query}")
            print(f"  top3={top3}")
            print(
                f"  retrieved={retrieved_id} "
                f"expected={hop.expected_document_id}"
            )
            print(
                f"  fact={extracted_fact} "
                f"expected_fact={hop.expected_fact}"
            )
            print(
                f"  qualifier={extracted_qualifier}"
            )

            state = RetrievalState(
                entity=extracted_fact,
                qualifiers=(
                    [extracted_qualifier]
                    if extracted_qualifier is not None
                    else []
                ),
                source_document_id=retrieved_id,
                evidence_text=retrieved_document.text,
            )
            print(f"  state={state.model_dump()}")
            print()

        task_hop_accuracy = hop_accuracy(
            retrieved_chain,
            expected_chain,
        )
        task_exact_chain = exact_chain_match(
            retrieved_chain,
            expected_chain,
        )
        task_fact_accuracy = fact_accuracy(
            extracted_facts,
            expected_facts,
        )

        final_fact = (
            extracted_facts[-1]
            if extracted_facts
            else None
        )
        answer_correct = (
            final_fact is not None
            and final_fact.casefold()
            == task.expected_answer.casefold()
        )

        total_hops += len(expected_chain)
        correct_hops += sum(
            retrieved == expected
            for retrieved, expected in zip(
                retrieved_chain,
                expected_chain,
            )
        )

        total_facts += len(expected_facts)
        correct_facts += sum(
            extracted is not None
            and extracted.casefold()
            == expected.casefold()
            for extracted, expected in zip(
                extracted_facts,
                expected_facts,
            )
        )

        exact_chains += int(task_exact_chain)
        correct_answers += int(answer_correct)

        print(
            f"HopAccuracy={task_hop_accuracy:.4f}"
        )
        print(
            f"ExactChainMatch={task_exact_chain:.4f}"
        )
        print(
            f"FactAccuracy={task_fact_accuracy:.4f}"
        )
        print(
            f"AnswerCorrect={float(answer_correct):.4f}"
        )
        print()

    print("Aggregate")
    print(f"tasks={len(tasks)}")
    print(f"hops={total_hops}")
    print(
        "HopAccuracy="
        f"{correct_hops / total_hops:.4f}"
    )
    print(
        "ExactChainMatchRate="
        f"{exact_chains / len(tasks):.4f}"
    )
    print(
        "FactAccuracy="
        f"{correct_facts / total_facts:.4f}"
    )
    print(
        "AnswerAccuracy="
        f"{correct_answers / len(tasks):.4f}"
    )


if __name__ == "__main__":
    main()
