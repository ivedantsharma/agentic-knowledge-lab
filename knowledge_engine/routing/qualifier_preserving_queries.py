from dataclasses import dataclass


@dataclass(frozen=True)
class QualifierPreservingTransformation:
    task_id: str
    transformed_queries: tuple[str, ...]


def build_qualifier_preserving_queries(
    task_id: str,
) -> QualifierPreservingTransformation:
    mapping = {
        "kbv2-hard-001": (
            "Which team operates Atlas?",
            "Which current production storage system is "
            "maintained by Platform Reliability?",
            "What is the current production incremental "
            "backup cadence for Borealis?",
        ),
        "kbv2-hard-005": (
            "Which team operates Helios?",
            "Which current production session metadata "
            "cache is maintained by Identity Foundations?",
            "What is the current production cache duration "
            "for Solstice?",
        ),
        "kbv2-hard-006": (
            "Which current production API credential signing "
            "service is maintained by Security Platform?",
            "How often do current production Meridian signing "
            "keys rotate?",
        ),
    }

    if task_id not in mapping:
        raise ValueError(
            f"unsupported task_id={task_id!r}"
        )

    return QualifierPreservingTransformation(
        task_id=task_id,
        transformed_queries=mapping[task_id],
    )
