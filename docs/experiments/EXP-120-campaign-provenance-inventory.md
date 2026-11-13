# EXP-120 — Campaign Benchmark Provenance and Reproducibility Inventory

## Question
Before comparative Phase 13 experiments, can we freeze the *actual* source files, verify task/evidence-family provenance and identify data/split contamination inherited from Phases 10–12?

## Hypothesis
The existing 22-document, 12-route, 17-policy-example benchmark is internally auditable and has six route evidence families. But Phase 11 and Phase 12 used different split definitions, so treating existing Phase 12 heldout as untouched for the new campaign would be misleading.

## Independent variable
No model or retriever variable is changed. EXP-120 is a reproducibility gate, not a performance comparison.

## Inputs
- `data/processed/knowledgebench_v2_hard_documents_v0.json`
- `data/processed/phase10_routing_pairs_v0.json`
- `data/processed/phase11_policy_dataset_v1.json`

No new labeled data, new model checkpoints, or new oracle results are generated. Record SHA-256 of each source file (bytes, not textual guesses).

## Checks / metrics
Count distinct documents, routes, families, policy examples; reject duplicate IDs and unknown supporting docs; check exact source question consistency; confirm that each route family stays in one Phase 11 split; report counts and split roles. Identify Phase 12's prior training family and inspected heldout families. **No scores or accuracies should be inferred from the manifest.**

## Controls and limitations
The old repository is tiny, contains related questions, and its test families have already been viewed. The audit is descriptive, not proof of a valid pristine unseen set. Source hashes change if serialized inputs change, which requires a new experiment manifest.

## Reproduce
```bash
uv run python scripts/run_phase13_campaign_inventory.py
uv run pytest
uv run ruff check .
```

## Acceptance
No duplicate IDs, no missing gold IDs, no mismatched join questions or family-to-split leakage within each source protocol; machine-checkable input hashes and marked reused families.

## Next
A frozen reproducible comparison matrix and baseline protocol before EXP-121; acquire untouched families before claimed learned-agent generalization.
