from knowledge_engine.graph.entity_type import (
    LexicalEntityTypeInferer,
)


def test_infers_team_from_group() -> None:
    inferer = LexicalEntityTypeInferer()

    result = inferer.infer(
        "group maintaining the cache"
    )

    assert result.entity_type == "team"


def test_infers_service_from_platform() -> None:
    inferer = LexicalEntityTypeInferer()

    result = inferer.infer(
        "storage platform for profiles"
    )

    assert result.entity_type == "service"


def test_abstains_without_type_cue() -> None:
    inferer = LexicalEntityTypeInferer()

    result = inferer.infer(
        "thing responsible for payroll"
    )

    assert result.entity_type is None


def test_abstains_on_conflicting_type_cues() -> None:
    inferer = LexicalEntityTypeInferer()

    result = inferer.infer(
        "team service for authentication"
    )

    assert result.entity_type is None
