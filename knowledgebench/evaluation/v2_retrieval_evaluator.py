from dataclasses import dataclass

from knowledgebench.tasks.v2_schema import (
    KnowledgeBenchV2Task,
)


@dataclass(frozen=True)
class KnowledgeBenchV2TaskReport:
    task_id: str
    supporting_recall_at_k: float
    reciprocal_rank: float
    evidence_chain_coverage: float
    distractor_hit: bool
    contradiction_hit: bool
    stale_hit: bool
    ambiguity_candidate_coverage: float
    retrieved_any: bool


@dataclass(frozen=True)
class KnowledgeBenchV2RetrievalReport:
    tasks: int
    answerable_tasks: int
    unanswerable_tasks: int
    mean_supporting_recall_at_k: float
    mean_reciprocal_rank: float
    mean_evidence_chain_coverage: float
    distractor_hit_rate: float
    contradiction_hit_rate: float
    stale_hit_rate: float
    mean_ambiguity_candidate_coverage: float
    unanswerable_retrieval_rate: float
    task_reports: list[KnowledgeBenchV2TaskReport]


def _reciprocal_rank(
    retrieved_ids: list[str],
    supporting_ids: set[str],
) -> float:
    for rank, document_id in enumerate(
        retrieved_ids,
        start=1,
    ):
        if document_id in supporting_ids:
            return 1.0 / rank
    return 0.0


def evaluate_v2_retrieval(
    tasks: list[KnowledgeBenchV2Task],
    retrieved_by_task: dict[str, list[str]],
    k: int,
) -> KnowledgeBenchV2RetrievalReport:
    if k <= 0:
        raise ValueError(
            "k must be positive"
        )

    task_reports: list[
        KnowledgeBenchV2TaskReport
    ] = []

    answerable_recall: list[float] = []
    answerable_rr: list[float] = []
    chain_coverages: list[float] = []

    distractor_hits: list[bool] = []
    contradiction_hits: list[bool] = []
    stale_hits: list[bool] = []
    ambiguity_coverages: list[float] = []
    unanswerable_retrieval: list[bool] = []

    for task in tasks:
        retrieved = retrieved_by_task.get(
            task.task_id,
            [],
        )[:k]
        retrieved_set = set(retrieved)

        if task.supporting_document_ids:
            supporting_recall = (
                len(
                    retrieved_set
                    & task.supporting_document_ids
                )
                / len(task.supporting_document_ids)
            )
            reciprocal_rank = _reciprocal_rank(
                retrieved,
                task.supporting_document_ids,
            )
            answerable_recall.append(
                supporting_recall
            )
            answerable_rr.append(
                reciprocal_rank
            )
        else:
            supporting_recall = 0.0
            reciprocal_rank = 0.0

        if task.evidence_chain:
            chain_coverage = (
                len(
                    retrieved_set
                    & set(task.evidence_chain)
                )
                / len(task.evidence_chain)
            )
            chain_coverages.append(
                chain_coverage
            )
        else:
            chain_coverage = 0.0

        distractor_hit = bool(
            retrieved_set
            & task.distractor_document_ids
        )
        contradiction_hit = bool(
            retrieved_set
            & task.contradicting_document_ids
        )
        stale_hit = bool(
            retrieved_set
            & task.stale_document_ids
        )
        if task.ambiguity_candidate_document_ids:
            ambiguity_candidate_coverage = (
                len(
                    retrieved_set
                    & task.ambiguity_candidate_document_ids
                )
                / len(
                    task.ambiguity_candidate_document_ids
                )
            )
            ambiguity_coverages.append(
                ambiguity_candidate_coverage
            )
        else:
            ambiguity_candidate_coverage = 0.0

        retrieved_any = bool(retrieved)

        if task.distractor_document_ids:
            distractor_hits.append(
                distractor_hit
            )
        if task.contradicting_document_ids:
            contradiction_hits.append(
                contradiction_hit
            )
        if task.stale_document_ids:
            stale_hits.append(
                stale_hit
            )
        if not task.should_answer:
            unanswerable_retrieval.append(
                retrieved_any
            )

        task_reports.append(
            KnowledgeBenchV2TaskReport(
                task_id=task.task_id,
                supporting_recall_at_k=(
                    supporting_recall
                ),
                reciprocal_rank=(
                    reciprocal_rank
                ),
                evidence_chain_coverage=(
                    chain_coverage
                ),
                distractor_hit=distractor_hit,
                contradiction_hit=(
                    contradiction_hit
                ),
                stale_hit=stale_hit,
                ambiguity_candidate_coverage=(
                    ambiguity_candidate_coverage
                ),
                retrieved_any=retrieved_any,
            )
        )

    answerable_tasks = sum(
        task.should_answer
        for task in tasks
    )
    unanswerable_tasks = (
        len(tasks) - answerable_tasks
    )

    return KnowledgeBenchV2RetrievalReport(
        tasks=len(tasks),
        answerable_tasks=answerable_tasks,
        unanswerable_tasks=unanswerable_tasks,
        mean_supporting_recall_at_k=(
            sum(answerable_recall)
            / len(answerable_recall)
            if answerable_recall
            else 0.0
        ),
        mean_reciprocal_rank=(
            sum(answerable_rr)
            / len(answerable_rr)
            if answerable_rr
            else 0.0
        ),
        mean_evidence_chain_coverage=(
            sum(chain_coverages)
            / len(chain_coverages)
            if chain_coverages
            else 0.0
        ),
        distractor_hit_rate=(
            sum(distractor_hits)
            / len(distractor_hits)
            if distractor_hits
            else 0.0
        ),
        contradiction_hit_rate=(
            sum(contradiction_hits)
            / len(contradiction_hits)
            if contradiction_hits
            else 0.0
        ),
        stale_hit_rate=(
            sum(stale_hits)
            / len(stale_hits)
            if stale_hits
            else 0.0
        ),
        mean_ambiguity_candidate_coverage=(
            sum(ambiguity_coverages)
            / len(ambiguity_coverages)
            if ambiguity_coverages
            else 0.0
        ),
        unanswerable_retrieval_rate=(
            sum(unanswerable_retrieval)
            / len(unanswerable_retrieval)
            if unanswerable_retrieval
            else 0.0
        ),
        task_reports=task_reports,
    )
