# EXP-120 Result — Campaign Source Provenance and Split Integrity

## Execution
- GitHub Actions push workflow on `main`: run **43491630184**, commit `f87c9552fc5abe36a2fa2fb5dc49aeb484335801`.
- `uv run pytest`: **390 passed in 16.97s**.
- `uv run ruff check .`: **All checks passed**.
- `uv run python scripts/run_phase13_campaign_inventory.py`: **PASS**.
- Inputs were read on-disk; no training, new gold labels, oracle tuning or model performance evaluation occurred.

## Immutable source fingerprints (SHA-256)
| Input file | Exact file-byte SHA-256 |
|---|---|
| `data/processed/knowledgebench_v2_hard_documents_v0.json` | `9015e8924fffcb461a7278c24e7f108d7a33377fcb6967d0f7bf0539fe9022be` |
| `data/processed/phase10_routing_pairs_v0.json` | `996514ff172e71756e300a9b43fc189603d14ba914da18e5c7cf12129d014ef2` |
| `data/processed/phase11_policy_dataset_v1.json` | `233e6d83a4607070d9937a3f302c27dd4a243b9373c4b692351a5f560bc3c549` |

## Corpus and task inventory
- **22** unique knowledge documents.
- **12** real routing tasks; **6** evidence families, each with **2** related queries.
- **17** Phase 11 labeled policy examples: **11 train, 3 dev, 3 heldout**.

| Routing evidence family | Task count | Phase 11 split | Prior Phase 12 role |
|---|---:|---|---|
| borealis_backup | 2 | dev | Inspected heldout |
| cirrus_retry | 2 | train | Training (route-003); route-004 same-family |
| meridian_rotation | 2 | heldout | Inspected heldout |
| nimbus_session | 2 | train | Inspected heldout |
| orion_logs | 2 | train | Inspected heldout |
| solstice_cache | 2 | train | Inspected heldout |

## Integrity checks
**PASS:** unique IDs, all routing gold-support IDs present among documents, source task question text matches its Phase 11 counterpart, and no source evidence family is split across supervised partitions.

## Critical interpretation
This is a *provenance/reproducibility gate*. The earlier Phase 12 test families were already inspected and should **not** be treated as pristine heldout families for future adaptive-policy tuning. Phase 11 and Phase 12 have different training/test splits and retriever/action protocols.

**No claim** is made about retrieval accuracy, trained-model generalization, confidence intervals, or the presence of a newly gathered unseen benchmark.

## Reproduction
```bash
uv run python scripts/run_phase13_campaign_inventory.py
uv run pytest
uv run ruff check .
```

CI now runs the provenance audit automatically on every push to `main` in `.github/workflows/ci.yml`. Re-record fingerprints and reassess splits whenever a source file changes.

## Decision
EXP-120 **complete**. Move to EXP-121's preregistered fixed-retriever baseline comparison under one frozen corpus/task/budget protocol; gather fresh independent evidence families **before** any later learned-policy transfer claim.
