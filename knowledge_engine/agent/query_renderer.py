from knowledge_engine.retrieval.state import RetrievalState


def render_state_query(
    template: str,
    state: RetrievalState,
) -> str:
    """Render a query template from structured retrieval state."""
    query = template

    if "{entity}" in query:
        if state.entity is None:
            raise ValueError(
                "query template requires entity "
                "but state.entity is empty"
            )

        query = query.replace(
            "{entity}",
            state.entity,
        )

    if "{qualifier}" in query:
        if not state.qualifiers:
            raise ValueError(
                "query template requires qualifier "
                "but state.qualifiers is empty"
            )

        query = query.replace(
            "{qualifier}",
            " ".join(state.qualifiers),
        )

    return query
