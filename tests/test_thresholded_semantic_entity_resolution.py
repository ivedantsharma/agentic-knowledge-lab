from knowledge_engine.graph.semantic_entity_resolution import (
    ThresholdedEntityResolutionResult,
)


def test_thresholded_result_can_represent_abstention() -> None:
    result = ThresholdedEntityResolutionResult(
        entity_id=None,
        score=0.2,
        accepted=False,
    )

    assert result.entity_id is None
    assert result.accepted is False
