# EXP-123 Result Record — Static versus Multi-Step Search

## Status
**Pretrained-model numerical run pending.** EXP-123 implementation has been committed directly on `main`, with deterministic fake-tool tests to verify the shared protocol. This file must not be interpreted as measured retrieval performance.

## Registered source and protocol
- `data/processed/phase4_ood_corpus_v0.jsonl`: existing Phase 4 development search corpus.
- `data/processed/phase4_planner_benchmark_v0.json`: four known and one out-of-distribution-intent multi-hop tasks.
- Frozen MiniLM `sentence-transformers/all-MiniLM-L6-v2` via the existing `DenseSearchTool` for every arm.
- `static_top3`: one original-question search, top-3 exposed.
- `static_top9`: one original-question search, top-9 exposed.
- `static_repeat3`: original question searched three times, top-3 per call (diagnostic cost control, not a strong optimized static multiqueury policy).
- `rule_agent3`: existing `RuleBasedPlanner`, up to three sequential top-3 searches, with *only top-1 document text* observed for subsequent planning.
- Primary: retrieval of all gold hop document IDs and gold Recall. Secondary: search calls, total hits, unique exposed IDs, repeated queries, stop/failure rate and query traces.
- Gold paths/answers are evaluation-only; model doesn't receive task hop labels.
- These are **previously inspected** Phase 4 tasks, not a pristine unseen-family evaluation; no broad generalization inference.

## Implementation CI validation

- GitHub Actions run `43503795790`, commit `0c72dad28a606f26bfd95d0d72bb1d687ff93a85`: **432 tests passed in 20.73s**, Ruff **All checks passed**; provenance audits ran successfully.
- Nine new EXP-123 tests cover the real 19-document/five-task source contract, one- vs nine-document exposure, three-call repeat baseline, the actual existing rule planner with fake backend, a gold-label isolation test, all-top-K evidence scoring, malformed outputs and invalid arms.
- CI uses a fake search backend and **does not** infer numerical results for the real MiniLM embedding model.

## Unfilled numerical results
**Do not invent or infer results.** Await actual stdout for:
```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_static_agentic_comparison.py
```

On completion, record source SHA-256, task counts, each task's retrieved hits and planner trace, per-arm mean Recall, full-evidence rate, calls, unique docs, failures, and whether any apparent gain survives the `static_top9` exposure control. No matched answer generator or wall-clock latency analysis is used.

## Known interpretation risks
- Even with the same search backend, one-shot top9 vs three top3 calls differ in query diversity, retrieval inference count and contextual observations.
- Repeating the same query three times is a weak, deliberately redundant static control; don't claim a decisive agentic-vs-best-static win from it.
- The historic RuleBasedPlanner uses rules tailored to this family of document patterns and may fail an unseen intent.
- The planner only observes top1, but evaluator counts all returned topK IDs, consistently across arms.
- This is retrieval-evidence quality, **not final-answer accuracy**.
