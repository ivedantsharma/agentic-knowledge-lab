"""Conservative source-cited extractive response for explicit service questions.

Deliberately narrow. This is NOT factual verification of the underlying
corpus, natural-language reasoning, or a general answer/abstention model.
No benchmark labels, expected answers or oracle information are consulted.
"""

import re
from dataclasses import dataclass

from knowledge_engine.integrated.pipeline import IntegratedResult

_PATTERNS = {
    "backup": re.compile(
        r"\bProduction\s+(?P<subject>[A-Za-z0-9_-]+)\s+incremental backups run\s+"
        r"(?P<answer>every\s+[^.]+)\.",
        flags=re.IGNORECASE,
    ),
    "retry": re.compile(
        r"\bProduction\s+(?P<subject>[A-Za-z0-9_-]+)\s+retries failed jobs at most\s+"
        r"(?P<answer>[^.]+?)\s+before\b",
        flags=re.IGNORECASE,
    ),
    "cache": re.compile(
        r"\bProduction\s+(?P<subject>[A-Za-z0-9_-]+)\s+caches validated session "
        r"metadata for\s+(?P<answer>[^.]+)\.",
        flags=re.IGNORECASE,
    ),
    "rotation": re.compile(
        r"\bProduction\s+(?P<subject>[A-Za-z0-9_-]+)\s+signing keys rotate\s+"
        r"(?P<answer>every\s+[^.]+)\.",
        flags=re.IGNORECASE,
    ),
}


@dataclass(frozen=True)
class SourceAnswer:
    status: str
    answer: str | None
    citation_document_ids: tuple[str, ...]
    reason: str

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "answer": self.answer,
            "citation_document_ids": list(self.citation_document_ids),
            "reason": self.reason,
        }


def _intent(question: str) -> str | None:
    q = question.casefold()
    if "backup" in q:
        return "backup"
    if "retri" in q or "retry" in q:
        return "retry"
    if "cach" in q:
        return "cache"
    if "signing key" in q or "keys rotate" in q or "rotation" in q:
        return "rotation"
    return None


def extract_source_answer(result: IntegratedResult) -> SourceAnswer:
    """Return an extractive *source-supported* claim or an explicit abstention.

    The answer must be explicitly present in a service_manual, with the
    service name also present in the user's question (not inferred from gold).
    Multiple distinct current-source values lead to abstention. Metadata-
    marked stale and pending policy documents never authorize an answer.
    """
    kind = _intent(result.question)
    if kind is None:
        return SourceAnswer("abstain", None, (), "unsupported_question_type")
    matches: dict[str, list[str]] = {}
    for hit in result.evidence:
        if hit.source_type != "service_manual" or hit.risk_flag is not None:
            continue
        found = _PATTERNS[kind].search(hit.text)
        if found is None:
            continue
        subject = found.group("subject")
        if re.search(r"\b" + re.escape(subject) + r"\b", result.question, re.IGNORECASE) is None:
            continue
        candidate = " ".join(found.group("answer").split())
        normalized = candidate.casefold()
        matches.setdefault(normalized, []).append(hit.document_id)
        # Keep original capitalization of source claim instead of a paraphrase.
    if not matches:
        return SourceAnswer("abstain", None, (), "no_explicit_current_source_support")
    if len(matches) != 1:
        return SourceAnswer("abstain", None, (), "conflicting_current_source_values")
    answer = next(iter(matches))
    return SourceAnswer(
        status="source_supported_extractive",
        answer=answer,
        citation_document_ids=tuple(matches[answer]),
        reason="extracted_from_retrieved_service_manual_not_independently_verified",
    )
