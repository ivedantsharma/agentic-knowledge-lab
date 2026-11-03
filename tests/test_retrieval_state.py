from knowledge_engine.retrieval.state import RetrievalState


def test_retrieval_state_stores_entity_and_qualifiers() -> None:
    state = RetrievalState(
        entity="Borealis",
        qualifiers=["production"],
        source_document_id="org_platform_reliability",
    )

    assert state.entity == "Borealis"
    assert state.qualifiers == ["production"]
    assert state.source_document_id == "org_platform_reliability"
