# EXP-013: Phase 3 Single-Hop Baseline

## Question

```text
What backup cadence is used by the storage system maintained by the team that operates Atlas?
```

## Gold evidence chain

```text
org_atlas
→ org_platform_reliability
→ manual_borealis
```

## One-shot dense ranking

| Rank | Document | Type | Score |
|---:|---|---|---:|
| 1 | distractor_atlas_backup | distractor | 0.595931 |
| 2 | org_atlas | expected | 0.577508 |
| 3 | org_platform_reliability | expected | 0.465678 |
| 4 | manual_borealis | expected | 0.440500 |
| 5 | distractor_team | distractor | 0.206562 |

## Interpretation

The top-ranked result is a distractor.

It matches surface terms from the question:
- Atlas
- backup

but it is not part of the required reasoning path.

The final answer-bearing document, `manual_borealis`, appears only at rank 4.

This shows a key multi-hop failure mode:

> A single query can over-weight words from different parts of a compositional question and retrieve a document that looks globally similar without satisfying the dependency chain.

## Next experiment

Execute the gold hop queries one at a time.

This does not test planning yet.

It tests whether decomposed retrieval can recover the intended evidence path when the search sequence is known.
