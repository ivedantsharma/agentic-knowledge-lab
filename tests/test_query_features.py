from knowledge_engine.routing.query_features import (
    extract_query_features,
)


def test_extracts_temporal_and_relational_features() -> None:
    features = extract_query_features(
        "What is the current production cadence for the "
        "service maintained by the team that operates Atlas?"
    )

    assert features.temporal_cue_count == 2
    assert features.relational_phrase_count >= 2
    assert features.has_explicit_current_cue is True
    assert features.has_multi_relation_proxy is True


def test_simple_single_entity_query_is_not_multi_relation() -> None:
    features = extract_query_features(
        "How many retries does Cirrus use?"
    )

    assert features.relational_phrase_count == 0
    assert features.has_multi_relation_proxy is False
