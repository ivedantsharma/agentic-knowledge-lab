from dataclasses import dataclass

from knowledge_engine.graph.schema import (
    ClaimGraph,
    EvidenceReference,
    GraphEntity,
    KnowledgeClaim,
)


@dataclass(frozen=True)
class GraphTraversalResult:
    start_entity_id: str
    relation_path: list[str]
    claim_ids: list[str]
    final_value: str
    evidence: list[EvidenceReference]


class ClaimGraphIndex:
    """Deterministic index for explicit claim-graph traversal."""

    def __init__(self, graph: ClaimGraph) -> None:
        self.graph = graph
        self.entities_by_id = {
            entity.entity_id: entity
            for entity in graph.entities
        }

        self.outgoing: dict[
            tuple[str, str],
            list[KnowledgeClaim],
        ] = {}

        for claim in graph.claims:
            key = (
                claim.subject_entity_id,
                claim.relation,
            )
            self.outgoing.setdefault(
                key,
                [],
            ).append(claim)

    def entity(self, entity_id: str) -> GraphEntity:
        try:
            return self.entities_by_id[entity_id]
        except KeyError as exc:
            raise ValueError(
                f"unknown entity_id={entity_id}"
            ) from exc

    def traverse(
        self,
        start_entity_id: str,
        relation_path: list[str],
    ) -> GraphTraversalResult:
        if not relation_path:
            raise ValueError(
                "relation_path must contain at least one relation"
            )

        self.entity(start_entity_id)

        current_entity_id = start_entity_id
        traversed_claim_ids: list[str] = []
        evidence: list[EvidenceReference] = []
        final_value: str | None = None

        for hop_index, relation in enumerate(
            relation_path
        ):
            candidates = self.outgoing.get(
                (current_entity_id, relation),
                [],
            )

            if not candidates:
                raise ValueError(
                    "no claim for "
                    f"subject={current_entity_id}, "
                    f"relation={relation}"
                )

            if len(candidates) > 1:
                raise ValueError(
                    "ambiguous claim for "
                    f"subject={current_entity_id}, "
                    f"relation={relation}"
                )

            claim = candidates[0]
            traversed_claim_ids.append(
                claim.claim_id
            )
            evidence.extend(claim.evidence)

            is_last_hop = (
                hop_index == len(relation_path) - 1
            )

            if claim.object_entity_id is not None:
                object_entity = self.entity(
                    claim.object_entity_id
                )

                if is_last_hop:
                    final_value = object_entity.name
                else:
                    current_entity_id = (
                        claim.object_entity_id
                    )
                continue

            if not is_last_hop:
                raise ValueError(
                    "literal claim cannot be traversed "
                    "before the final hop"
                )

            final_value = claim.object_value

        if final_value is None:
            raise ValueError(
                "traversal completed without a final value"
            )

        return GraphTraversalResult(
            start_entity_id=start_entity_id,
            relation_path=relation_path,
            claim_ids=traversed_claim_ids,
            final_value=final_value,
            evidence=evidence,
        )
