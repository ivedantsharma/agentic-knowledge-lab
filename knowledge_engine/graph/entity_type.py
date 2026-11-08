from dataclasses import dataclass

from knowledge_engine.graph.entity_resolution import (
    normalize_entity_text,
)


@dataclass(frozen=True)
class EntityTypeInferenceResult:
    entity_type: str | None
    matched_cue: str | None


class LexicalEntityTypeInferer:
    """Infer coarse graph entity type from explicit mention cues."""

    def __init__(self) -> None:
        self.type_cues = {
            "team": {
                "team",
                "group",
                "organization",
                "org",
                "squad",
            },
            "service": {
                "service",
                "system",
                "platform",
                "application",
                "app",
                "worker",
                "cache",
            },
        }

    def infer(
        self,
        mention_text: str,
    ) -> EntityTypeInferenceResult:
        normalized = normalize_entity_text(
            mention_text
        )

        if not normalized:
            raise ValueError(
                "mention_text must contain searchable text"
            )

        tokens = set(
            normalized.split()
        )

        matches = [
            (entity_type, cue)
            for entity_type, cues in self.type_cues.items()
            for cue in cues
            if cue in tokens
        ]

        matched_types = {
            entity_type
            for entity_type, _cue in matches
        }

        if not matches:
            return EntityTypeInferenceResult(
                entity_type=None,
                matched_cue=None,
            )

        if len(matched_types) > 1:
            return EntityTypeInferenceResult(
                entity_type=None,
                matched_cue=None,
            )

        entity_type = next(
            iter(matched_types)
        )
        cue = next(
            cue
            for candidate_type, cue in matches
            if candidate_type == entity_type
        )

        return EntityTypeInferenceResult(
            entity_type=entity_type,
            matched_cue=cue,
        )



class FirstCueEntityTypeInferer(LexicalEntityTypeInferer):
    """Infer type from the earliest explicit type cue in mention order."""

    def infer(
        self,
        mention_text: str,
    ) -> EntityTypeInferenceResult:
        normalized = normalize_entity_text(
            mention_text
        )

        if not normalized:
            raise ValueError(
                "mention_text must contain searchable text"
            )

        tokens = normalized.split()

        cue_to_type = {
            cue: entity_type
            for entity_type, cues in self.type_cues.items()
            for cue in cues
        }

        for token in tokens:
            entity_type = cue_to_type.get(
                token
            )
            if entity_type is not None:
                return EntityTypeInferenceResult(
                    entity_type=entity_type,
                    matched_cue=token,
                )

        return EntityTypeInferenceResult(
            entity_type=None,
            matched_cue=None,
        )
