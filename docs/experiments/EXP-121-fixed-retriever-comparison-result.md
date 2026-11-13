# EXP-121 Result — Controlled BM25 / Dense / Hybrid Retrieval Comparison

## Status
**Complete: full real-model numerical output supplied and recorded**, with the code/metrics tests validated by GitHub CI.

## Reproducibility and controls
- Command: `uv run python scripts/run_phase13_fixed_retriever_comparison.py`, run in the user's workspace after EXP-121 implementation.
- Source-file SHA-256 values verified against EXP-120 prior to loading MiniLM.
- Frozen 22-document corpus, 12 previously inspected paired routing tasks, six evidence families.
- Fixed: `sentence-transformers/all-MiniLM-L6-v2`, BM25 `k1=1.5, b=.75`, Hybrid reciprocal-rank fusion `rrf_k=60`.
- Equal K budgets: `1,2,3,5`; no query transformation or learned policy.
- Bootstrap: 10,000 seeded family-level draws, seed 121; this is **not** independent model-training replication.
- GitHub CI on `main` commit `766a6b4110c89777de045ef0a28d92d0054c48d4`: **400 passed in 16.19s**, Ruff passed, EXP-120 data audit passed.
- Hugging Face warned about unauthenticated requests. MiniLM loaded all 103 weight objects successfully. No numerical error in the experiment driver.

## Measured retrieval metrics

| Method | K | Supporting Recall@K | MRR@K | Gold-complete fraction |
|---|---:|---:|---:|---:|
| BM25 | 1 | 0.6667 | 0.6667 | 0.6667 |
| BM25 | 2 | 0.9167 | 0.7917 | 0.9167 |
| BM25 | 3 | 1.0000 | 0.8194 | 1.0000 |
| BM25 | 5 | 1.0000 | 0.8194 | 1.0000 |
| Dense MiniLM | 1 | 0.5833 | 0.5833 | 0.5833 |
| Dense MiniLM | 2 | 0.9167 | 0.7500 | 0.9167 |
| Dense MiniLM | 3 | 1.0000 | 0.7778 | 1.0000 |
| Dense MiniLM | 5 | 1.0000 | 0.7778 | 1.0000 |
| Hybrid RRF | 1 | 0.6667 | 0.6667 | 0.6667 |
| Hybrid RRF | 2 | **1.0000** | **0.8333** | **1.0000** |
| Hybrid RRF | 3 | 1.0000 | 0.8333 | 1.0000 |
| Hybrid RRF | 5 | 1.0000 | 0.8333 | 1.0000 |

Hybrid reaches all gold support at K2 on this particular 12-task set. BM25 and dense need K3 for full coverage. All three reach full gold evidence at K3. MRR ceases to change after K3 for these ranked results. The relative quality of ranking, not answer correctness, is measured.

## Family-clustered paired MRR@3 differences

| Comparison | Mean Hybrid minus baseline | Descriptive 95% bootstrap interval | Families |
|---|---:|---:|---:|
| Hybrid − BM25 | +0.0139 | [−0.1111, +0.1250] | 6 |
| Hybrid − Dense | +0.0556 | [+0.0000, +0.1389] | 6 |

Family-level `Hybrid − BM25` MRR@3:
- `borealis_backup`: +0.2500
- `cirrus_retry`: −0.2500
- `meridian_rotation`: 0.0000
- `nimbus_session`: 0.0000
- `orion_logs`: 0.0000
- `solstice_cache`: +0.0833

Family-level `Hybrid − Dense` MRR@3:
- `borealis_backup`: 0.0000
- `cirrus_retry`: 0.0000
- `meridian_rotation`: +0.0833
- `nimbus_session`: 0.0000
- `orion_logs`: 0.0000
- `solstice_cache`: +0.2500

**Interpretation:** Hybrid is the best fixed strategy by this benchmark's point estimate and is particularly context-efficient at K2, but the mean MRR advantage above BM25 is small and the family interval spans zero. Only six previously inspected families are available; the bootstrap is descriptive rather than strong statistical proof. No hypothesis-test p-values are claimed.

## Historical replication
EXP-121's measured K3 BM25 MRR 0.8194, Dense MRR 0.7778, and Hybrid MRR 0.8333, all with Recall@3 = 1.0000, match EXP-096/097's historical numerical results. EXP-121 additionally measures K1/2/5 and records family-clustered uncertainty.

## Failure analysis and decision
- **Saturation:** all methods have recall 1.0 at K3, making this benchmark too easy to demonstrate large improvements in overall recall.
- **Family heterogeneity:** Hybrid gains on Borealis but regresses on Cirrus versus BM25. A single averaged win hides this.
- **Uncertain architecture advantage:** Hybrid minus BM25 interval includes zero.
- **Limited independence:** paired paraphrases are correlated, so uncertainty uses six families rather than 12 pseudo-independent questions.
- **Development exposure:** these families were used in Phases 10–12; do not report external/untouched generalization.

**Decision:** Keep fixed Hybrid RRF and BM25 as baselines. Do not promote a sophisticated retriever router from these small deltas. Move to Phase 13 EXP-122 representation-architecture feasibility and controlled ablation, with explicit task comparability/coverage checks.

## Reproduce
```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_fixed_retriever_comparison.py
```

No learned policy, generated-answer correctness, real latency study or broad domain transfer was evaluated.
