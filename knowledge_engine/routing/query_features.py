from dataclasses import dataclass
import re


_TEMPORAL_TERMS = {
    "current",
    "latest",
    "production",
    "previous",
    "pending",
}

_RELATIONAL_PHRASES = (
    "maintained by",
    "operates",
    "operated by",
    "team that",
    "service maintained by",
    "system maintained by",
)


@dataclass(frozen=True)
class QueryFeatures:
    token_count: int
    capitalized_token_count: int
    temporal_cue_count: int
    relational_phrase_count: int
    has_explicit_current_cue: bool
    has_multi_relation_proxy: bool


def extract_query_features(
    question: str,
) -> QueryFeatures:
    tokens = re.findall(
        r"[A-Za-z0-9_-]+",
        question,
    )

    lowercase_tokens = [
        token.casefold()
        for token in tokens
    ]

    capitalized_token_count = sum(
        1
        for index, token in enumerate(tokens)
        if index > 0
        and token[:1].isupper()
    )

    temporal_cue_count = sum(
        1
        for token in lowercase_tokens
        if token in _TEMPORAL_TERMS
    )

    normalized_question = (
        " ".join(question.casefold().split())
    )
    relational_phrase_count = sum(
        normalized_question.count(phrase)
        for phrase in _RELATIONAL_PHRASES
    )

    return QueryFeatures(
        token_count=len(tokens),
        capitalized_token_count=(
            capitalized_token_count
        ),
        temporal_cue_count=temporal_cue_count,
        relational_phrase_count=(
            relational_phrase_count
        ),
        has_explicit_current_cue=(
            "current" in lowercase_tokens
        ),
        has_multi_relation_proxy=(
            relational_phrase_count >= 2
        ),
    )
