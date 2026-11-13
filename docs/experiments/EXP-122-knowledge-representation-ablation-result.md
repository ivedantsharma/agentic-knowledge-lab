# EXP-122 Result — Gate A: Representation Substrate Feasibility

## Status
**Gate A implemented and CI validated; the actual fair cross-representation architecture ablation is BLOCKED pending a shared task/source mapping.** EXP-122 as a whole is not complete.

## Validation
- GitHub Actions on `main` for commit `fd70d2dea9ba134b02781922fe8c29d53b70f638`, run `43497907988`.
- **407 tests passed in 18.70s**, Ruff **All checks passed**, EXP-120 source provenance audit PASS.
- Seven EXP-122 unit/smoke tests validated actual Phase 5/6 input schemas, source references, graph claim IDs, duplicate entity rejection, input integrity, and the no-crosswalk warning.
- CI exercised the real-data `main()` path through pytest output-capture. Separate full user-local stdout has not yet been supplied.

## Observed task and substrate differences
| Property | Phase 5 hierarchy | Phase 6 graph |
|---|---|---|
| Source | `phase5_long_section_documents_v0.json` | `phase6_branching_claim_graph_v0.json` |
| Source units | 6 structured documents with sections | entity and claim records |
| Tasks | 3 evidence-span questions | 4 graph path/answer questions |
| Existing pipeline | `CoarseToFineHierarchicalRetriever` | `ClaimGraphQAEngine` |
| Current metric | evidence retention; returned context words | entity/path/answer/provenance correctness |
| Exact paired source-task IDs | **None shared** | **None shared** |
| Exact question-text overlap | **None observed** | **None observed** |

The Gate A driver also reports the unique source content hashes, actual entity/claim counts, shared exact expected answers, and a boolean for a complete task crosswalk. Those detailed values should be archived from a full independent driver run rather than guessed.

## Scientific conclusion
The old Phase 5 and Phase 6 percentages cannot estimate a causal advantage of hierarchical over graph retrieval. Comparing them would confound representation with task difficulty, available evidence, answer-vs-span scoring and resource usage.

No new benchmark examples or model results were generated. Gate B must **not** start without a common labeled source of facts, paired tasks and a matched-budget evaluation contract. This is a negative feasibility result, not a failed model.

## Reproduce
```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_representation_substrate_audit.py
```

## Next
Freeze a cross-representation document/claim mapping and shared question set, then compare flat/hierarchy/graph using evidence coverage, grounded answer correctness, provenance and resource metrics at comparable budgets. Keep the existing Phase 5 and 6 datasets as development history, not independent heldout test sets.
