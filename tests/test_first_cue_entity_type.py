from knowledge_engine.graph.entity_type import (
    FirstCueEntityTypeInferer,
)


def test_first_cue_prefers_team_before_service() -> None:
    inferer = FirstCueEntityTypeInferer()

    result = inferer.infer(
        "team operating the Atlas authentication service"
    )

    assert result.entity_type == "team"
    assert result.matched_cue == "team"


def test_first_cue_prefers_group_before_cache() -> None:
    inferer = FirstCueEntityTypeInferer()

    result = inferer.infer(
        "group maintaining the production session metadata cache"
    )

    assert result.entity_type == "team"
    assert result.matched_cue == "group"


def test_first_cue_keeps_service_phrase() -> None:
    inferer = FirstCueEntityTypeInferer()

    result = inferer.infer(
        "worker platform running production asynchronous workloads"
    )

    assert result.entity_type == "service"
    assert result.matched_cue == "worker"
