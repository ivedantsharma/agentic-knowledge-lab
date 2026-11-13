# EXP-122 Result — Gate A: Representation Substrate Feasibility

## Status
**Gate A implemented and CI validated; the actual fair cross-representation architecture ablation is BLOCKED pending a shared task/source mapping.** EXP-122 as a whole is not complete.

## Validation
- GitHub Actions on `main` for commit `fd70d2dea9ba134b02781922fe8c29d53b70f638`, run `43497907988`.
- **407 tests passed in 18.70s**, Ruff **All checks passed**, EXP-120 source provenance audit PASS.
- Seven EXP-122 unit/smoke tests validated actual Phase 5/6 input schemas, source references, graph claim IDs, duplicate entity rejection, input integrity, and the no-crosswalk warning.
- CI exercised the real-data `main()` path through pytest output-capture. Full user-local stdout supplied for `uv run python scripts/run_phase13_representation_substrate_audit.py` and the values below were directly observed.

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

### Full user-observed Gate A values
- Phase 5: **6 structured documents, 9 sections, 3 tasks**.
- Phase 6: **11 entities, 15 claims, 4 tasks**.
- `shared_task_ids=()`, `shared_exact_questions=()`, `shared_expected_answers=()`, `complete_paired_task_crosswalk=False`.
- **BLOCKED**: no complete paired task mapping exists.

### Source SHA-256 hashes (exact user-observed output)
| Source | SHA-256 |
|---|---|
| `data/processed/phase5_long_section_documents_v0.json` | `a66964b95752fc8bb50a1c2789c548d4618cd33145c4962adbdb2a9937c21d89` |
| `data/processed/phase5_long_section_tasks_v0.json` | `6f77a40b281a9c8d3e424e2d44be4a7236829eb9b37612a549123aca89a5e5dc` |
| `data/processed/phase6_branching_claim_graph_v0.json` | `4e3b26bd9dfbc57f57eb501132279f50e96be87e7db96ba7838d552a2669718e` |
| `data/processed/phase6_graph_tasks_v0.json` | `767c9b0b2a3ea42d3d08407e1d095062790f770917d1e2452632adc5c9f0db9e` |

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
