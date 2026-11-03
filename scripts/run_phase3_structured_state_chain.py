import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.retrieval.fact_extractor import (
    extract_fact,
)
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
from scripts.cosine_similarity_exercise import (
    cosine_similarity,
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CORPUS_PATH = Path(
    "data/processed/phase3_multihop_corpus_v2.jsonl"
)
TASK_PATH = Path(
    "data/processed/phase3_multihop_tasks_v3.json"
)


def render_state_query(
    template: str,
    state: RetrievalState,
) -> str:
    query = template

    if "{entity}" in query:
        if state.entity is None:
            raise ValueError(
                "query template requires entity "
                "but state.entity is empty"
            )

        query = query.replace(
            "{entity}",
            state.entity,
        )

    if "{qualifier}" in query:
        if not state.qualifiers:
            raise ValueError(
                "query template requires qualifier "
                "but state.qualifiers is empty"
            )

        query = query.replace(
            "{qualifier}",
            " ".join(state.qualifiers),
        )

    return query


def rank_documents(
    query: str,
    documents,
    document_embeddings,
    model: SentenceTransformer,
) -> list[tuple[str, float]]:
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

    return scored


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
        state = RetrievalState()
        retrieved_chain: list[str] = []
        expected_chain: list[str] = []
        extracted_facts: list[str | None] = []
        expected_facts: list[str] = []

        print(task.task_id)
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
            retrieved_id, score = top3[0]
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
            print(f"  state_before={state.model_dump()}")
            print(f"  rendered_query={rendered_query}")
            print(f"  top3={top3}")
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
                f"  extracted_fact={extracted_fact}"
            )
            print(
                f"  extracted_qualifier="
                f"{extracted_qualifier}"
            )
            print(
                f"  expected_fact={hop.expected_fact} "
                f"fact={fact_status}"
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

            print(f"  state_after={state.model_dump()}")
            print()

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
