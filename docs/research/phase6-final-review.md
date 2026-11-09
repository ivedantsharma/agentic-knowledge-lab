# Phase 6 Final Review

## Status

Complete.

Phase 6 is closed as a mechanism-validation and failure-analysis phase.

The final hard stress benchmark is intentionally not perfect.

That negative result is part of the closeout rather than something to tune away.

## Central question

> Can explicit entity, relation, and claim structure improve retrieval when the answer depends on relationships rather than only textual similarity?

For the controlled synthetic benchmarks:

> Yes, explicit claim structure provides reliable traversal, path constraints, and provenance when the system enters the graph at the correct entity.

The largest remaining weakness is semantic entity entry and abstention, not graph traversal.

## What was built

### Claim/evidence graph

- typed entities,
- typed claims,
- literal and entity-valued objects,
- evidence references,
- graph-integrity validation.

### Deterministic graph traversal

- outgoing claim index,
- exact relation traversal,
- evidence accumulation,
- ambiguity rejection.

### Entity resolution

- canonical name matching,
- alias matching,
- longest-match handling,
- lexical abstention,
- semantic entity profiles,
- type-constrained semantic ranking,
- confidence gating,
- hybrid lexical/semantic resolver.

### Graph path search

- bounded simple-path enumeration,
- cycle avoidance,
- literal-valued path termination,
- path profiles,
- semantic path ranking,
- path-score margins.

### Reusable QA engine

```text
ClaimGraphQAEngine
```

with injectable entity resolvers.

## Experiment progression

### EXP-053

Gold entity + gold relation path.

```text
AnswerAccuracy=1.0000
PathAccuracy=1.0000
ProvenanceCoverage=1.0000
```

Validated graph representation and deterministic traversal.

### EXP-054 / EXP-055

Lexical entity linking and stress testing.

Canonical names, aliases, overlapping names, and abstention behaved correctly.

### EXP-056

Whole-question semantic entity ranking.

Negative result:

```text
SemanticHit@1=0.5000
```

The ranker partly performed answer retrieval instead of entity linking.

### EXP-057

Mention-span semantic ranking.

```text
MentionSpanHit@1=1.0000
```

This isolated query representation as the main failure in EXP-056.

### EXP-058

Held-out thresholded entity resolution.

```text
ResolvableEntityAccuracy=0.5000
AbstentionAccuracy=1.0000
```

The threshold rejected unrelated examples but allowed wrong related-node links.

### EXP-059

Gold type-constrained entity ranking.

```text
TypedResolvableAccuracy=1.0000
TypedAbstentionAccuracy=1.0000
```

This proved type compatibility was a useful missing signal.

### EXP-060 / EXP-061

Automatic type inference and repair.

First-cue type inference fixed mixed-cue parsing:

```text
TypeInferenceAccuracy:
0.6667 → 1.0000
```

but one correct semantic candidate remained below the global threshold.

### EXP-062

Semantic relation-path selection over a branching graph.

```text
PathSelectionAccuracy=1.0000
AnswerAccuracy=1.0000
AvgCandidatePaths=2.00
```

The Atlas path had a small margin over a legacy-storage distractor.

### EXP-063

Explicit-name end-to-end graph QA.

Reported:

```text
EntityLinkAccuracy=1.0000
PathSelectionAccuracy=1.0000
AnswerAccuracy=1.0000
ProvenanceCoverage=1.0000
```

This validated component composition.

### EXP-064

Hard hybrid end-to-end stress.

```text
AnswerableEndToEndSuccessRate=0.5000
EntityResolutionAccuracy=0.5000
PathSelectionAccuracy=0.5000
AnswerAccuracy=0.5000
ProvenanceCoverage=0.5000
AbstentionAccuracy=0.5000
FalsePositiveAnswerRate=0.5000
```

This exposed the true remaining weakness.

Two answerable tasks abstained before path search because semantic entity scores fell below the fixed threshold.

One unrelated team query was incorrectly linked into the graph and produced a valid but irrelevant answer.

## Main research lessons

### 1. Graph traversal is not the same as graph access

A graph can be perfectly structured and still fail if the user query is linked to the wrong node.

### 2. Provenance should be part of the data model

Evidence is not an afterthought.

Each claim should know why it exists.

### 3. Entity linking and answer retrieval are different objectives

Embedding the whole question can rank the answer entity instead of the mentioned entity.

### 4. Symbolic constraints complement semantic similarity

Type filtering repaired related-node confusion that semantic ranking alone could not.

### 5. Cosine similarity is not calibrated confidence

One global threshold caused both:

- false abstention,
- false positive entry.

### 6. Graph structure constrains relation planning

Enumerating graph-valid paths prevented impossible relation sequences.

### 7. Accuracy alone hides path uncertainty

The Atlas near-distractor path margin was small despite correct top-1 selection.

### 8. Stage-level metrics matter

EXP-064's path/answer metrics fell only because entity resolution failed upstream.

Conditioned on successful entry, path selection remained correct.

### 9. Negative results should stop over-tuning

The correct response to EXP-064 is not to lower the threshold until the six tasks pass.

The failure is evidence that the confidence policy needs a better benchmark and method.

## Reference architecture

```text
Question
→ lexical entity match
→ optional typed semantic fallback
→ confidence / abstention
→ bounded graph-valid path enumeration
→ MiniLM path ranking
→ top claim path
→ answer + provenance
```

## What Phase 6 deliberately does not solve

- production-scale graph retrieval,
- calibrated entity confidence,
- robust mention extraction,
- complex entity linking,
- temporal claims,
- contradictory claims,
- qualifier-aware duplicate relations,
- learned relation planning,
- graph/text adaptive routing.

These are appropriate future research directions rather than reasons to keep tuning the Phase 6 synthetic benchmark.

## Why Phase 6 stops here

The phase now contains:

- explicit representation,
- deterministic mechanics,
- controlled oracle baselines,
- entity-linking ablations,
- semantic failure analysis,
- symbolic constraints,
- path-search baselines,
- branching distractors,
- end-to-end integration,
- hard negative stress,
- reusable implementation,
- explicit failure taxonomy,
- architecture decision record.

Further tuning on the same small benchmark would reduce scientific value.

## Next phase

Phase 7:

# KnowledgeBench v2 — Hard Retrieval Evals

The next focus is no longer improving this one graph benchmark.

It is building a broader, harder evaluation suite covering:

- multi-hop reasoning,
- distractors,
- ambiguity,
- contradictions,
- stale/temporal knowledge,
- unanswerable questions.

That benchmark will give later retrieval and agent policies a more credible test bed.
