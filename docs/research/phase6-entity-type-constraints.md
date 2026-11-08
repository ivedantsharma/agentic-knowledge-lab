# Phase 6: Entity Type as a Retrieval Constraint

Semantic similarity can retrieve a strongly related node that fills the wrong semantic role.

Example:

    "group that runs the Atlas authentication service"

The graph contains both:

    Platform Reliability : team
    Atlas                : service

Both are semantically related, but "group" signals that the referent should be a team.

Type-constrained ranking applies a symbolic compatibility filter before semantic ranking:

    expected type
    -> compatible entities only
    -> semantic ranking
    -> confidence gate

EXP-059 uses the gold type deliberately. If it repairs the failures, then automatic type inference becomes justified as the next separate component.
