from dataclasses import dataclass


def normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


def answer_matches(
    predicted: str | None,
    expected: str,
) -> bool:
    if predicted is None:
        return False

    predicted_normalized = normalize_text(predicted)
    expected_normalized = normalize_text(expected)

    return expected_normalized in predicted_normalized


@dataclass(frozen=True)
class PlannerTaskResult:
    task_id: str
    expected_answer: str
    final_answer: str | None
    stopped: bool
    planner_failed: bool
    max_steps_exhausted: bool
    search_steps: int
    retrieved_document_ids: list[str]
    final_evidence_document_id: str

    @property
    def answer_correct(self) -> bool:
        return answer_matches(
            self.final_answer,
            self.expected_answer,
        )

    @property
    def final_evidence_retrieved(self) -> bool:
        return (
            self.final_evidence_document_id
            in self.retrieved_document_ids
        )

    @property
    def premature_stop(self) -> bool:
        return (
            self.stopped
            and not self.final_evidence_retrieved
        )


@dataclass(frozen=True)
class PlannerAggregateMetrics:
    tasks: int
    answer_accuracy: float
    planner_failure_rate: float
    stopped_rate: float
    stop_precision: float
    premature_stop_rate: float
    search_success_rate: float
    average_search_steps: float
    max_step_exhaustion_rate: float


def aggregate_planner_results(
    results: list[PlannerTaskResult],
) -> PlannerAggregateMetrics:
    if not results:
        raise ValueError(
            "planner evaluation requires at least one result"
        )

    tasks = len(results)
    stopped = [
        result
        for result in results
        if result.stopped
    ]

    correct_stops = sum(
        result.answer_correct
        for result in stopped
    )

    stop_precision = (
        correct_stops / len(stopped)
        if stopped
        else 0.0
    )

    return PlannerAggregateMetrics(
        tasks=tasks,
        answer_accuracy=(
            sum(result.answer_correct for result in results)
            / tasks
        ),
        planner_failure_rate=(
            sum(result.planner_failed for result in results)
            / tasks
        ),
        stopped_rate=(
            len(stopped) / tasks
        ),
        stop_precision=stop_precision,
        premature_stop_rate=(
            sum(result.premature_stop for result in results)
            / tasks
        ),
        search_success_rate=(
            sum(
                result.final_evidence_retrieved
                for result in results
            )
            / tasks
        ),
        average_search_steps=(
            sum(result.search_steps for result in results)
            / tasks
        ),
        max_step_exhaustion_rate=(
            sum(
                result.max_steps_exhausted
                for result in results
            )
            / tasks
        ),
    )
