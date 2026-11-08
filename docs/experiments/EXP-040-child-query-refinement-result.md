# EXP-040 Result: Child Query Refinement

## Aggregate result

```text
DocumentHit@1=1.0000
OriginalChildHit@1=0.6667
RefinedChildHit@1=0.6667
```

## Per-task result

### Atlas

Original and refined queries both retrieve Token Rotation.

### Borealis

Original and refined queries both retrieve Backup Policy.

### Cirrus

Original:

```text
Where are Cirrus jobs sent after exhausting all retries?
→ Retry Policy
```

Refined:

```text
destination after all retry attempts
→ Retry Policy
```

The relevant section remains:

```text
Dead Letter Handling
```

## Interpretation

The Cirrus failure is not repaired by a simple deterministic relation-focused query rewrite.

This suggests the bottleneck is the child scorer's semantic discrimination rather than only query phrasing.

## Important observation

The refined query lowers absolute similarity scores for Atlas and Borealis while preserving the same top section.

This reinforces that cosine score magnitude should not be interpreted as calibrated confidence.

## Conclusion

Do not keep tuning query rewrites on this tiny benchmark.

The next controlled experiment should keep:

- parent routing,
- query,
- candidate sections,

fixed, and change only the child scoring model.

Use a cross-encoder reranker over the sections inside the selected parent document.