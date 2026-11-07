import re

from knowledge_engine.retrieval.state import RetrievalState

_RELATION_PATTERNS: list[tuple[str, str]] = [
    (
        r"operated by the (.+?) team",
        "entity",
    ),
    (
        r"maintains the (.+?) storage system",
        "entity",
    ),
    (
        r"maintains the (.+?) worker platform",
        "entity",
    ),
    (
        r"maintains the (.+?) cache service",
        "entity",
    ),
    (
        r"maintains the (.+?) signing service",
        "entity",
    ),
    (
        r"Incremental backups run (every [^.]+)",
        "answer",
    ),
    (
        r"retried at most (.+?) before",
        "answer",
    ),
    (
        r"cached for (.+?)[.]",
        "answer",
    ),
    (
        r"rotate (every [^.]+)",
        "answer",
    ),
]

_QUALIFIER_PATTERN = re.compile(
    r"for (production|staging|development|legacy)\b",
    flags=re.IGNORECASE,
)


def parse_retrieval_observation(
    document_id: str,
    text: str,
) -> RetrievalState:
    """Convert retrieved evidence into structured planner state."""
    extracted_entity: str | None = None

    for pattern, _kind in _RELATION_PATTERNS:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match is not None:
            extracted_entity = match.group(1).strip()
            break

    qualifier_match = _QUALIFIER_PATTERN.search(text)

    qualifiers = (
        [qualifier_match.group(1).lower()]
        if qualifier_match is not None
        else []
    )

    return RetrievalState(
        entity=extracted_entity,
        qualifiers=qualifiers,
        source_document_id=document_id,
        evidence_text=text,
    )
