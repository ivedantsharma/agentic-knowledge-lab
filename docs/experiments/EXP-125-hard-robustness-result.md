# EXP-125 Result — Hard Retrieval Robustness

## Status
**Full pretrained-model numerical run pending.** The experiment's protocol, grader, real-input driver and isolated tests are implemented on `main`. Do not interpret test or mock-encoder results as measured MiniLM performance.

## Data and controls
- Existing hard v0 KnowledgeBench documents/tasks, plus four Phase 9 injection cases **for inventory only**.
- BM25, frozen MiniLM Dense, and Hybrid RRF (k=60) all rank the same unchanged documents for the same unchanged questions.
- K=1,3,5, with evaluator-only source labels.
- Independently grade gold-support recall/complete evidence, conditional exposure to stale/contradiction/distractor documents, and unanswerable nonempty retrieval.
- **No answer generator, abstention/thresholding policy, or injection-attack model is executed.** These cannot be scored from retrieval IDs.
- Sources were previously inspected and are development material, not a new heldout evaluation.

## Numerical results
**Not yet supplied.** Capture the exact stdout from:
```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_hard_robustness_comparison.py
```

On receipt, archive the exact source hashes and sample counts, all K/method aggregate values, per-task hits, risk-denominator counts and failures. Do not infer stronger generalization from the existing source tasks. The inability to evaluate safe abstention or prompt-injection resistance from retrieval-only runs must remain an explicit limitation.

## Progress
EXP-125 is **in progress**, with real-model scores and scientific closeout outstanding. EXP-124 is blocked on protocol/data/checkpoint prerequisites. Phase 13 stays at **4/6 (~67%)** completed full studies until these gates are resolved.

## Implementation validation

GitHub Actions run `43507480873`, source commit `a0882fe815673502cadf1c0defbea6001fbef03c`: **447 tests passed in 16.30s**, Ruff **All checks passed**, existing EXP-120 source-provenance, EXP-122 common representation and EXP-124 comparability audits passed. The eight new EXP-125 tests cover actual hard-v0 and Phase 9 inventory counts, all three retrieval adapters using a deterministic fake embedder, K-monotonicity, evaluator-only unanswerable treatment, source integrity, invalid rankings and conditional risk denominators. **These are not observed real MiniLM risk or recall scores.**
