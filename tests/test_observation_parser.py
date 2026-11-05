from knowledge_engine.agent.observation_parser import (
    parse_retrieval_observation,
)


def test_parse_entity_and_qualifier() -> None:
    state = parse_retrieval_observation(
        "org-platform",
        (
            "Platform Reliability maintains the Borealis "
            "storage system for production customer data."
        ),
    )

    assert state.entity == "Borealis"
    assert state.qualifiers == ["production"]


def test_parse_final_answer() -> None:
    state = parse_retrieval_observation(
        "manual-borealis",
        (
            "For the production Borealis service, "
            "Incremental backups run every six hours."
        ),
    )

    assert state.entity == "every six hours"
