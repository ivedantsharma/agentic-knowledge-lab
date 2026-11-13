# EXP-121 — Fixed Retriever Architecture Comparison Under a Frozen Protocol

## Question
On the identical Phase 10 paired-routing corpus and evidence-family structure, how do fixed BM25, MiniLM dense, and RRF hybrid rank relevant evidence across K=1,2,3,5? Is an apparent improvement over the strongest fixed retriever robust across evidence families?

## Pre-run hypotheses
1. Hybrid MRR@3 will be competitive with BM25 and dense, as observed in EXP-096/097.
2. Recall at K=3 may saturate, masking ranking differences at K=1 or 2.
3. Even if Hybrid has a higher mean MRR, there are only **six independent evidence families**; family-level uncertainty may include zero.
4. No retriever should be declared universally best from these already inspected development tasks.

## Controlled design
- **Only independent variable:** fixed retrieval strategy: BM25 (repo defaults k1=1.5,b=.75), MiniLM cosine dense, or RRF of their full rankings with rrf_k=60.
- **Frozen inputs:** exact files from EXP-120, 22 docs and 12 paired routes / six families; validate SHA-256 before running.
- **Fixed model:** `sentence-transformers/all-MiniLM-L6-v2`, same original Phase 10 model identifier. This is not a model architecture sweep or a new seed-trained model.
- **Equal top-K:** each strategy uses the SAME K in {1,2,3,5}, no query rewriting or adaptive budgeting.
- **Gold labels:** consulted ONLY in metrics after rankings are built, never in rankers.
- **Metrics:** supporting Recall@K, MRR@K, complete gold coverage, per-family mean MRR; paired family-level Hybrid-vs-BM25 and Hybrid-vs-Dense deltas at K3.
- **Uncertainty:** explicit percentile **cluster bootstrap** over the six families, resampling whole families, seed 121, 10,000 draws, 95% interval. Descriptive only with six families, not a significance guarantee.
- **Computational seeds:** model inference is deterministic/frozen (not five independent training seeds). Bootstrap repetitions are not independent model trials. Report this distinction.
- **Confounds:** exact model weights may vary by cache/revision; record resolved installed model revision if available and command environment. No inference latency claims without timing controls.
- **Negative control:** identical strategy rankings give exactly zero paired delta and [0,0] cluster interval.
- **Consistency:** replicate original EXP-096 metrics at K3 if model revision and ranking tie behavior match; if not, disclose drift.

## Workflow and file structure
- `knowledgebench/evaluation/phase13_retriever_comparison.py`: pure ranking/metrics, family-bootstrap utilities; no model download or gold-visible retriever.
- `scripts/run_phase13_fixed_retriever_comparison.py`: real-corpus loading, MiniLM embeddings, BM25, RRF, input hash gate and output.
- `tests/test_phase13_retriever_comparison.py`: hand-checkable metrics, no leakage, family-unit bootstrap and fake deterministic embedder.
- `docs/experiments/EXP-121-fixed-retriever-comparison-result.md`: populated with real measured numerical stdout **only after the full script is run**.

## Decision gate
Do not train a sophisticated router merely because a few examples have different winners. If the strongest fixed strategy is competitive and family uncertainty is wide, prioritize new evidence families / more discriminative tasks. Preserve the EXP-097 routing-headroom finding.

## Run
```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_fixed_retriever_comparison.py
```
