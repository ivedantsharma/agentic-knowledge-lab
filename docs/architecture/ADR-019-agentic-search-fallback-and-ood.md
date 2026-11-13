# ADR-019 — Treat Agentic Search as a Fallible Policy and Require Strong Static Fallbacks

## Status
Accepted, following measured EXP-123 results.

## Context
EXP-123 evaluated a four-arm, same-`DenseSearchTool`, five-question Phase 4 **development** benchmark. One-shot static top3, one-shot static top9, three repeated static top3 calls and the existing evidence-conditioned RuleBasedPlanner (up to three calls) were compared using the same 19 documents and evidence-chain labels. The policy receives only the top1 document's text for its next state; the independent evaluator counts all returned topK IDs.

## Observed results
| Arm | Mean Recall | Full gold evidence | Calls per task | Failure fraction |
|---|---:|---:|---:|---:|
| Static top3 | 0.8000 | 3/5 | 1.0 | 0/5 |
| Static top9 | 1.0000 | 5/5 | 1.0 | 0/5 |
| Static repeat3 | 0.8000 | 3/5 | 3.0 | 0/5 |
| Rule agent3 | 0.8000 | 4/5 | 2.0 | **1/5** |

The rule planner recovered missing support evidence on familiar three-hop tasks, but failed *before issuing any search* for `ood-001`, asking where exhausted failed jobs are sent. One-shot top3 found all gold evidence for that task. Static top9 achieved complete evidence support on all five tasks, at a larger per-query returned-document exposure than the rule agent.

## Decision
1. Do not promote a multi-step planner simply because it can solve familiar chains. Demonstrate an advantage against strong *context-exposure* baselines and budget-matched static controls.
2. An unrecognized intent must not cause total retrieval failure when original-question search is available. New production-oriented controllers should have an explicit, auditable fallback to a safe unchanged-query search, subject to abstention and safety constraints.
3. Account separately for returned hits, unique documents, number of tool calls, compute/latency and whether the next-step policy actually saw each document.
4. Keep task-pattern-specific handcrafted rules distinct from learned or generally adaptive policies; evaluate on independent source families and unseen intents before broad claims.
5. Do not compare end-to-end answer accuracy without the same answer generator for all methods, and do not infer compute savings from fewer documents exposed.
6. Preserve `ood-001` as a *previously inspected failure diagnostic*, not a fresh heldout generalization task.

## Rejected interpretations
- “Agentic beats static”: it failed OOD intent; top9 was 5/5.
- “Repeat3 proves planning beats equal budget”: repeated identical searches are a weak control and do not match unique information opportunity.
- “A single call is always cheaper”: top9 and top3/three-call arms retrieve different amounts of evidence and have no controlled latency measurements.
- “An unfamiliar intent failed only because retrieval was weak”: failure occurred before issuing the first search, in the rule planner's initial-query generation.

## Consequences
EXP-124 cannot use familiar-task planner success or historic cross-protocol learned scores as evidence that new SFT/RL policies generalize. Future agent controllers should expose well-defined STOP, fallback, action masking and evaluator-only gold, with honest failure and cost reporting.

See `docs/experiments/EXP-123-static-vs-agentic-search-result.md` and `docs/experiments/EXP-124-learned-policy-comparison.md`.
