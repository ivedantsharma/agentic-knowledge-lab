import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.retrieval.fact_extractor import (
    extract_fact,
)
from knowledgebench.documents.loader import load_documents_jsonl
from knowledgebench.metrics.multihop import (
    exact_chain_match,
    fact_accuracy,
    hop_accuracy,
)
from knowledgebench.tasks.multihop_loader import (
    load_multihop_tasks_json,
)
from scripts.cosine_similarity_exercise import (
    cosine_similarity,
)
from scripts.run_phase3_gold_fact_chaining import (
    render_query,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CORPUS_PATH = Path(
    "data/processed/phase3_multihop_corpus_v0.jsonl"
)
TASK_PATH = Path(
    "data/processed/phase3_multihop_tasks_v1.json"
)


def retrieve_top1(
    query: str,
    documents,
    document_embeddings,
    model: SentenceTransformer,
) -> tuple[str, float]:
    query_embedding = model.encode(query).tolist()

    scored = [
        (
            document.document_id,
            cosine_similarity(
                query_embedding,
                embedding.tolist(),
            ),
        )
        for document, embedding in zip(
            documents,
            document_embeddings,
        )
    ]

    scored.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return scored[0]


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

    for task in tasks:
        retrieved_chain: list[str] = []
        expected_chain: list[str] = []
        extracted_facts: list[str | None] = []
        expected_facts: list[str] = []
        previous_fact: str | None = None

        print(task.task_id)
        print(f"question={task.question}")
        print()

        for hop in task.hops:
            template = hop.query_template or hop.query

            rendered_query = render_query(
                template,
                previous_fact,
            )

            retrieved_id, score = retrieve_top1(
                rendered_query,
                documents,
                document_embeddings,
                model,
            )

            retrieved_document = document_by_id[
                retrieved_id
            ]

            if hop.extraction_pattern is None:
                raise ValueError(
                    "extraction_pattern is required "
                    "for extracted-fact chaining"
                )

            extracted_fact = extract_fact(
                retrieved_document.text,
                hop.extraction_pattern,
            )

            retrieved_chain.append(retrieved_id)
            expected_chain.append(
                hop.expected_document_id
            )
            extracted_facts.append(extracted_fact)
            expected_facts.append(
                hop.expected_fact
            )

            retrieval_status = (
                "CORRECT"
                if retrieved_id == hop.expected_document_id
                else "WRONG"
            )
            fact_status = (
                "CORRECT"
                if extracted_fact is not None
                and extracted_fact.casefold()
                == hop.expected_fact.casefold()
                else "WRONG"
            )

            print(f"hop={hop.hop_index + 1}")
            print(f"  template={template}")
            print(
                f"  previous_fact={previous_fact}"
            )
            print(
                f"  rendered_query={rendered_query}"
            )
            print(
                f"  expected_document="
                f"{hop.expected_document_id}"
            )
            print(
                f"  retrieved_document={retrieved_id}"
            )
            print(
                f"  score={score:.6f} "
                f"retrieval={retrieval_status}"
            )
            print(
                f"  extraction_pattern="
                f"{hop.extraction_pattern}"
            )
            print(
                f"  extracted_fact={extracted_fact}"
            )
            print(
                f"  expected_fact={hop.expected_fact} "
                f"fact={fact_status}"
            )
            print()

            previous_fact = extracted_fact

            if (
                hop.hop_index < len(task.hops) - 1
                and previous_fact is None
            ):
                print(
                    "Stopping: no intermediate fact "
                    "was extracted."
                )
                break

        print(
            f"retrieved_chain={retrieved_chain}"
        )
        print(
            f"expected_chain={expected_chain}"
        )
        print(
            "HopAccuracy="
            f"{hop_accuracy(retrieved_chain, expected_chain):.4f}"
        )
        print(
            "ExactChainMatch="
            f"{exact_chain_match(retrieved_chain, expected_chain):.4f}"
        )
        print(
            "FactAccuracy="
            f"{fact_accuracy(extracted_facts, expected_facts):.4f}"
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

        print(f"final_answer={final_fact}")
        print(
            f"expected_answer={task.expected_answer}"
        )
        print(
            "AnswerCorrect="
            f"{float(answer_correct):.4f}"
        )
        print()


if __name__ == "__main__":
    main()
