import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentence_transformers import SentenceTransformer

from knowledge_engine.retrieval.bm25 import BM25Retriever
from knowledge_engine.retrieval.hybrid import reciprocal_rank_fusion
from knowledge_engine.retrieval.vector_math import cosine_similarity
from knowledge_engine.rl.retrieval_environment import (
    RetrievalEpisode,
    RetrievalRLAction,
    total_return,
)
from knowledgebench.documents.v2_schema import KnowledgeBenchV2Document
from knowledgebench.tasks.routing_schema import RoutingBenchmarkTask


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DOCS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")
TASKS = Path("data/processed/phase10_routing_pairs_v0.json")


def get_ranking() -> tuple[RoutingBenchmarkTask, list[str]]:
    documents = [
        KnowledgeBenchV2Document.model_validate(item)
        for item in json.loads(DOCS.read_text(encoding="utf-8"))
    ]
    tasks = [
        RoutingBenchmarkTask.model_validate(item)
        for item in json.loads(TASKS.read_text(encoding="utf-8"))
    ]
    task = next(task for task in tasks if task.task_id == "route-003")
    ids = [document.document_id for document in documents]
    texts = [document.text for document in documents]

    bm25_rank = [
        doc_id
        for doc_id, _score in BM25Retriever(ids, texts).rank(
            task.question, top_k=len(ids)
        )
    ]
    encoder = SentenceTransformer(MODEL_NAME)
    document_vectors = encoder.encode(texts)
    query_vector = encoder.encode(task.question).tolist()
    dense_scores = [
        (doc_id, cosine_similarity(query_vector, vector.tolist()))
        for doc_id, vector in zip(ids, document_vectors)
    ]
    dense_scores.sort(key=lambda row: row[1], reverse=True)
    ranking = [
        doc_id
        for doc_id, _score in reciprocal_rank_fusion(
            [bm25_rank, [doc_id for doc_id, _score in dense_scores]],
            top_k=len(ids),
        )
    ]
    return task, ranking


def run_episode(
    name: str,
    task: RoutingBenchmarkTask,
    ranking: list[str],
    actions: list[RetrievalRLAction],
) -> None:
    episode = RetrievalEpisode(
        question=task.question,
        ranked_ids=ranking,
        supporting_ids=set(task.supporting_document_ids),
    )
    transitions = []
    print(name)
    for action in actions:
        transition = episode.step(action)
        transitions.append(transition)
        print(
            f"  action={action.value} "
            f"new_docs={transition.new_document_count} "
            f"new_support={transition.new_support_count} "
            f"reward={transition.reward:+.2f} "
            f"visible_ids={transition.next_observation.retrieved_ids}"
        )
    print(f"  total_return={total_return(transitions):.2f}")
    print()


def main() -> None:
    task, ranking = get_ranking()
    print("Phase 12 EXP-111 — Retrieval Rewards and Trajectories")
    print(f"task={task.task_id}")
    print(f"ranked_top5={ranking[:5]}")
    print("Gold labels are evaluator-only, never part of policy observations.")
    print()
    run_episode(
        "Premature stop policy",
        task,
        ranking,
        [RetrievalRLAction.SEARCH_K1, RetrievalRLAction.STOP],
    )
    run_episode(
        "Evidence-aware continuation (oracle diagnostic, not a learned policy)",
        task,
        ranking,
        [
            RetrievalRLAction.SEARCH_K1,
            RetrievalRLAction.SEARCH_K2,
            RetrievalRLAction.STOP,
        ],
    )


if __name__ == "__main__":
    main()
