from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class GraphEntity(BaseModel):
    entity_id: str
    name: str
    entity_type: str
    aliases: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("entity_id", "name", "entity_type")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("entity fields must not be blank")
        return cleaned


class EvidenceReference(BaseModel):
    document_id: str
    evidence_text: str
    section_title: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("document_id", "evidence_text")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("evidence fields must not be blank")
        return cleaned

    @field_validator("section_title")
    @classmethod
    def validate_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("section_title must not be blank")
        return cleaned


class KnowledgeClaim(BaseModel):
    claim_id: str
    subject_entity_id: str
    relation: str
    object_entity_id: str | None = None
    object_value: str | None = None
    evidence: list[EvidenceReference] = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "claim_id",
        "subject_entity_id",
        "relation",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("claim fields must not be blank")
        return cleaned

    @field_validator("object_entity_id", "object_value")
    @classmethod
    def validate_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("claim object must not be blank")
        return cleaned

    @model_validator(mode="after")
    def validate_exactly_one_object(self) -> "KnowledgeClaim":
        has_entity = self.object_entity_id is not None
        has_value = self.object_value is not None

        if has_entity == has_value:
            raise ValueError(
                "claim must have exactly one of "
                "object_entity_id or object_value"
            )

        return self


class ClaimGraph(BaseModel):
    entities: list[GraphEntity]
    claims: list[KnowledgeClaim]
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_graph_integrity(self) -> "ClaimGraph":
        entity_ids = [
            entity.entity_id
            for entity in self.entities
        ]
        claim_ids = [
            claim.claim_id
            for claim in self.claims
        ]

        if len(entity_ids) != len(set(entity_ids)):
            raise ValueError("duplicate entity_id")

        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("duplicate claim_id")

        known_entities = set(entity_ids)

        for claim in self.claims:
            if claim.subject_entity_id not in known_entities:
                raise ValueError(
                    "claim subject must reference an existing entity"
                )

            if (
                claim.object_entity_id is not None
                and claim.object_entity_id not in known_entities
            ):
                raise ValueError(
                    "claim object_entity_id must reference "
                    "an existing entity"
                )

        return self
