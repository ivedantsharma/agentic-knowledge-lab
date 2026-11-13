# EXP-121 Result Record — Fixed Retriever Architecture Comparison

## Status
**Implementation and CI validated; full MiniLM numerical run pending user workspace execution.**

## GitHub CI validation
- `main` commit `766a6b4110c89777de045ef0a28d92d0054c48d4`, push workflow run `43494408666`.
- `uv run pytest`: **400 passed in 16.19s**.
- `uv run ruff check .`: **All checks passed**.
- EXP-120 provenance audit CI step: **PASS**.
- Ten new tests in `tests/test_phase13_retriever_comparison.py` validated hand-computed recall/MRR/coverage, source-family paired differences, 10,000-draw seeded bootstrap mechanics, zero-difference control and malformed inputs.
- **CI intentionally does not call MiniLM `SentenceTransformer.encode`** in the EXP-121 end-to-end script. Therefore tests do not establish numerical BM25/Dense/Hybrid outcomes on the frozen dataset.

## Frozen protocol
- 22 documents, 12 previously inspected paired questions, six evidence families; all input hashes verified against EXP-120.
- `BM25Retriever` defaults k1=1.5, b=.75.
- `sentence-transformers/all-MiniLM-L6-v2` dense cosine ranking.
- Reciprocal rank fusion of complete BM25/Dense rankings with rrf_k=60.
- K ∈ {1,2,3,5}; identical documents and questions per strategy.
- Family-clustered bootstrap, 10,000 draws, seed 121; resamples whole two-query evidence families, **not** independent training runs.

## Numerical result status
**Not yet measured by the EXP-121 full benchmark driver in the user workspace.** Do not invent Recall@K, MRR, completion, deltas, or confidence intervals.

Historical reference (EXP-096/097, **not a new EXP-121 measurement**): at K3, BM25 MRR 0.8194, Dense MRR 0.7778, Hybrid MRR 0.8333; all Recall@3 1.0000. These historical figures are a replication target, not substitute evidence.

## Reproduce and archive
```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_fixed_retriever_comparison.py
```

After capturing stdout, record per-strategy metrics for each K, paired family differences, 95% family-bootstrap intervals, observed comparison with historical EXP-096, and any model-version or ranking drift.

## Scientific interpretation and limits
- EXP-121's completed CI validates code behavior on synthetic hand-checkable examples and invariant dataset fingerprints, not real MiniLM numerical retrieval.
- The dataset has already been used in Phases 10–12, so its performance is **development replication**, not untouched heldout generalization.
- A family bootstrap with six clusters is descriptive and does not demonstrate statistically significant superiority.
- Success on retrieval metrics is not proof of final-answer quality or robust learned-agent reasoning.

## Next
Once numerical driver results are captured, decide whether further architecture comparisons are identifiable on the tiny corpus. Expand the benchmark with truly independent evidence families before policy optimization or broad statistical claims.
