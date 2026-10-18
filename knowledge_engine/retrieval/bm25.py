import math
import re
from collections import Counter

TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")


def tokenize(text: str) -> list[str]:
    """Tokenize text for the Phase 1 BM25 baseline."""
    return TOKEN_PATTERN.findall(text.lower())


class BM25Retriever:
    """Small BM25 implementation for controlled baseline experiments."""

    def __init__(
        self,
        document_ids: list[str],
        document_texts: list[str],
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        if len(document_ids) != len(document_texts):
            raise ValueError("document_ids and document_texts must have equal length")

        self.document_ids = document_ids
        self.k1 = k1
        self.b = b

        self.tokenized_documents = [
            tokenize(text)
            for text in document_texts
        ]
        self.term_frequencies = [
            Counter(tokens)
            for tokens in self.tokenized_documents
        ]

        self.document_lengths = [
            len(tokens)
            for tokens in self.tokenized_documents
        ]

        self.average_document_length = (
            sum(self.document_lengths) / len(self.document_lengths)
            if self.document_lengths
            else 0.0
        )

        self.document_frequency: Counter[str] = Counter()

        for tokens in self.tokenized_documents:
            for token in set(tokens):
                self.document_frequency[token] += 1

    def _idf(self, term: str) -> float:
        document_count = len(self.document_ids)
        document_frequency = self.document_frequency.get(term, 0)

        return math.log(
            1
            + (
                document_count - document_frequency + 0.5
            )
            / (
                document_frequency + 0.5
            )
        )

    def _score_document(self, query_tokens: list[str], document_index: int) -> float:
        if self.average_document_length == 0:
            return 0.0

        frequencies = self.term_frequencies[document_index]
        document_length = self.document_lengths[document_index]

        score = 0.0

        for term in query_tokens:
            term_frequency = frequencies.get(term, 0)

            if term_frequency == 0:
                continue

            denominator = term_frequency + self.k1 * (
                1
                - self.b
                + self.b
                * document_length
                / self.average_document_length
            )

            score += self._idf(term) * (
                term_frequency * (self.k1 + 1)
                / denominator
            )

        return score

    def rank(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        """Return document IDs and BM25 scores ranked highest first."""
        if top_k <= 0:
            return []

        query_tokens = tokenize(query)

        scored = [
            (
                document_id,
                self._score_document(query_tokens, index),
            )
            for index, document_id in enumerate(self.document_ids)
        ]

        scored.sort(key=lambda item: item[1], reverse=True)

        return scored[:top_k]
