# Phase 14 — Integrated Development Benchmark: Observed Result

## Status
**CI-observed CPU-only development diagnostic, not new heldout validation.** The integrated engine and narrow extractive source-answer gate execute, but the planner fallback behavior shows that the cross-phase integration is **not yet robust**.

## Reproduction and provenance
GitHub Actions run `43589688328` on commit `a151c8e30c78d14dc4c77a422ffca845af2240ef`: **478 tests passed in 13.14s**, Ruff clean, integrated benchmark step passed.

```bash
uv run python scripts/run_phase14_integrated_benchmark.py
```

Inputs are exactly the reused Phase 7 KnowledgeBench hard v0 documents (22) and questions (10: six answerable, four unanswerable).

- Corpus SHA-256: `9015e8924fffcb461a7278c24e7f108d7a33377fcb6967d0f7bf0539fe9022be`
- Tasks SHA-256: `3c61ed176940a81a63ac74f42f3734aaeedac46c2c0268bf487a7e290119ea6e`

## Real development measurements

| Metric | Static BM25 Top3 | Auto rule-planner with original-query fallback |
|---|---:|---:|
| Answerable tasks | 6 | 6 |
| Unanswerable tasks | 4 | 4 |
| Mean supporting-document recall | 0.7778 | 0.8889 |
| Complete gold evidence fraction | 0.6667 | 0.6667 |
| Exact/normalized extractive answer correct among answerable | **0.3333 (2/6)** | **0.3333 (2/6)** |
| Abstained on answerable tasks | 0.6667 (4/6) | 0.6667 (4/6) |
| Abstained on unanswerable tasks | 1.0000 (4/4) | 1.0000 (4/4) |
| Mean unique evidence docs | 3.0000 | 3.3000 |
| Mean search calls | 1.0000 | 1.6000 |
| Planner fallback rate (all tasks) | 0.0000 | **1.0000 (10/10)** |

**Critical caveats:**
- Static uses one Top3 query. Auto may do up to three Top3 planner calls **plus an original-query fallback** (up to four calls), so recall values are **NOT a fair matched-budget planner effectiveness comparison**.
- The extractor supports a few explicitly named direct service queries only. It returns `source_supported_extractive`, not independently verified knowledge. It correctly extracted `five times` for `kbv2-hard-007` and `every six hours` for `kbv2-hard-010`; the remaining four answerable tasks were abstained on.
- Abstaining on all four already-known unanswerable cases does NOT establish calibrated abstention or zero false-positive risk on real unseen questions. With 4/6 answerable abstentions, the method also has substantial incomplete service coverage.
- **All ten auto-mode tasks required fallback.** Eight intents were not natively recognized or resolved; the two complex three-hop cases exhausted the planner-search budget. The rule planner and this hard corpus follow different text/query patterns. Fallback prevents an outright empty-result error but does NOT constitute successful planning.
- No LLM answer-generation, new evidence families, independent model verification, paired injection test, matched wall-clock cost, or valid SFT/RL comparison was performed.

## Engineering conclusions

1. Keep the original-question fallback; EXP-123's prior zero-search OOD failure is avoided at the *retrieval availability* level.
2. Do **not** promote the template rule planner to a working general adaptive search engine. Every current benchmark task required fallback, despite the extra queries.
3. Separate evidence recall from actual answer/abstention correctness and retrieval cost.
4. A narrow source-extractive mode is useful as a transparent demonstration, but cannot be represented as a broadly accurate knowledge assistant.
5. For subsequent Phase 14 work, implement or swap in a planner capable of supporting the corpus's real source patterns and ensure a strictly matched-budget baseline. Add source-aware conflict and time handling before considering verified answer claims.

## Phase 14 milestone disposition

- **14.0 architecture contract:** implemented.
- **14.1 integrated retrieval pipeline/fallback:** implemented and tested; broad planner effectiveness NOT established.
- **14.2 narrow source-extraction/abstention prototype:** implemented and measured, but **not complete as a general verifier/abstainer**.
- **14.3 benchmark integration diagnostic:** real CI results documented, but end-to-end quality claims NOT established.
- **14.4 HTML/CLI demo, 14.5 reproducibility, 14.6 portfolio and 14.7 handoff:** being developed and need independent validation/closeout.

Honest milestone reporting matters: tested prototypes are not the same as completed research-validation gates.
