import re
from dataclasses import dataclass

from knowledge_engine.graph.schema import (
    ClaimGraph,
    GraphEntity,
)


def normalize_entity_text(value: str) -> str:
    return " ".join(
        re.findall(
            r"[a-z0-9]+",
            value.casefold(),
        )
    )


@dataclass(frozen=True)
class EntityResolutionResult:
    entity_id: str
    matched_surface: str
    match_type: str


class LexicalEntityResolver:
    """Resolve explicitly mentioned graph entities by name or alias."""

    def __init__(self, graph: ClaimGraph) -> None:
        self.entities = graph.entities

        self.surfaces: list[
            tuple[str, str, str]
        ] = []

        for entity in self.entities:
            self._add_surface(
                entity,
                entity.name,
                "name",
            )

            for alias in entity.aliases:
                self._add_surface(
                    entity,
                    alias,
                    "alias",
                )

        self.surfaces.sort(
            key=lambda item: len(item[1]),
            reverse=True,
        )

    def resolve(
        self,
        question: str,
    ) -> EntityResolutionResult:
        normalized_question = normalize_entity_text(
            question
        )

        if not normalized_question:
            raise ValueError(
                "question must contain searchable text"
            )

        matches = [
            (
                entity_id,
                normalized_surface,
                surface,
                match_type,
            )
            for (
                entity_id,
                normalized_surface,
                surface,
                match_type,
            ) in self.surfaces
            if self._contains_surface(
                normalized_question,
                normalized_surface,
            )
        ]

        if not matches:
            raise ValueError(
                "no graph entity mentioned in question"
            )

        longest_length = max(
            len(item[1])
            for item in matches
        )

        longest_matches = [
            item
            for item in matches
            if len(item[1]) == longest_length
        ]

        entity_ids = {
            item[0]
            for item in longest_matches
        }

        if len(entity_ids) != 1:
            raise ValueError(
                "ambiguous entity mention in question"
            )

        best = longest_matches[0]

        return EntityResolutionResult(
            entity_id=best[0],
            matched_surface=best[2],
            match_type=best[3],
        )

    def _add_surface(
        self,
        entity: GraphEntity,
        surface: str,
        match_type: str,
    ) -> None:
        normalized = normalize_entity_text(
            surface
        )

        if not normalized:
            raise ValueError(
                "entity name/alias must contain searchable text"
            )

        self.surfaces.append(
            (
                entity.entity_id,
                normalized,
                surface,
                match_type,
            )
        )

    @staticmethod
    def _contains_surface(
        normalized_question: str,
        normalized_surface: str,
    ) -> bool:
        padded_question = (
            f" {normalized_question} "
        )
        padded_surface = (
            f" {normalized_surface} "
        )
        return padded_surface in padded_question
