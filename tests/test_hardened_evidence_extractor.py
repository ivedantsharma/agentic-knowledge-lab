from knowledge_engine.agent.hardened_evidence_extractor import (
    HardenedEvidenceExtractor,
)
from knowledge_engine.agent.qwen_continuation_planner import (
    QwenContinuationPlanner,
)


def make_extractor(
    output: str,
) -> HardenedEvidenceExtractor:
    planner = object.__new__(
        QwenContinuationPlanner
    )
    planner._generate = lambda _instruction: output

    return HardenedEvidenceExtractor(
        planner=planner
    )


def test_hardened_extractor_returns_answer() -> None:
    extractor = make_extractor(
        "ten minutes"
    )

    assert extractor.extract_or_abstain(
        "How long?",
        "Cached for ten minutes.",
    ) == "ten minutes"


def test_hardened_extractor_maps_insufficient_to_none() -> None:
    extractor = make_extractor(
        "INSUFFICIENT"
    )

    assert extractor.extract_or_abstain(
        "How long?",
        "No duration present.",
    ) is None
