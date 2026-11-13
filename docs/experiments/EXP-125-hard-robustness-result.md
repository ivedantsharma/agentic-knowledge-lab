# EXP-125 Result — Hard Retrieval Robustness

## Status
**Partial real pretrained-model stdout archived: complete BM25/Dense rows and partial Hybrid results. Full Hybrid aggregate and EXP-125 closeout pending.** The experiment's protocol, grader, real-input driver and isolated tests are implemented on `main`. Do not interpret test or mock-encoder results as measured MiniLM performance.

## Data and controls
- Existing hard v0 KnowledgeBench documents/tasks, plus four Phase 9 injection cases **for inventory only**.
- BM25, frozen MiniLM Dense, and Hybrid RRF (k=60) all rank the same unchanged documents for the same unchanged questions.
- K=1,3,5, with evaluator-only source labels.
- Independently grade gold-support recall/complete evidence, conditional exposure to stale/contradiction/distractor documents, and unanswerable nonempty retrieval.
- **No answer generator, abstention/thresholding policy, or injection-attack model is executed.** These cannot be scored from retrieval IDs.
- Sources were previously inspected and are development material, not a new heldout evaluation.

## Partial full-model numerical results — user-supplied stdout, truncated

**Partial real-model run observed on 2026-11-14**: The user supplied the real MiniLM runner's stdout through the first five Hybrid RRF tasks (`kbv2-hard-001` through `kbv2-hard-005`), ending during `hybrid_rrf` K5 for `kbv2-hard-005`. All **10 BM25 tasks** and **10 Dense tasks** at K1, K3 and K5 are visible; Hybrid tasks 006–010 and the entire final aggregate section are **not in the supplied transcript**. Therefore **EXP-125 is not yet closed** and no full Hybrid comparison may be claimed.

### Observed data fingerprints, configuration and scale

- Encoder: `sentence-transformers/all-MiniLM-L6-v2`; 103 weight objects loaded successfully, with a nonfatal unauthenticated Hugging Face warning.
- Source: 22 existing documents, 10 hard tasks (6 answerable, 4 unanswerable), K = (1,3,5).
- Existing Phase 9 injection pairs: 4 (**inventory only**).
- `data/processed/knowledgebench_v2_hard_documents_v0.json`: SHA-256 `9015e8924fffcb461a7278c24e7f108d7a33377fcb6967d0f7bf0539fe9022be`.
- `data/processed/knowledgebench_v2_hard_tasks_v0.json`: SHA-256 `3c61ed176940a81a63ac74f42f3734aaeedac46c2c0268bf487a7e290119ea6e`.
- `data/processed/phase9_prompt_injection_pairs_v0.json`: SHA-256 `8cedd0675f37a31ca8995cea40267acd7a454852708a304e211e903abb248b21`.

### Independently calculated from the complete visible BM25 and Dense per-task rows

| Method | K | Mean supporting Recall@K, 6 answerable tasks | Tasks with all support | Distractor exposure, labeled n=2 | Contradiction exposure, labeled n=2 | Stale exposure, labeled n=3 |
|---|---:|---:|---:|---:|---:|---:|
| BM25 | 1 | 0.4444 | 1/6 | 0/2 | 0/2 | 1/3 |
| BM25 | 3 | 0.7778 | 4/6 | 1/2 | 0/2 | 3/3 |
| BM25 | 5 | 0.7778 | 4/6 | 2/2 | 1/2 | 3/3 |
| Dense | 1 | 0.5000 | 2/6 | 1/2 | 0/2 | 1/3 |
| Dense | 3 | 0.7500 | 3/6 | 1/2 | 2/2 | 2/3 |
| Dense | 5 | 0.8611 | 4/6 | 2/2 | 2/2 | 3/3 |

The risk denominators refer **only** to tasks carrying the particular risk label. The four unanswerable tasks all retrieved at least one document for both methods at all shown K values; this **does not evaluate abstention correctness**. For the two ambiguous tasks, both methods retrieved one of two candidate documents at K1 and both candidates by K3.

#### Individual failure diagnostics

- `kbv2-hard-001` multi-hop Atlas/Borealis: BM25 support recall remained 1/3 through K5 and selected labeled stale at K3 and labeled distractor at K5. Dense recovered 3/3 support by K5 but also exposed the labeled distractor at K1 and stale evidence by K5.
- `kbv2-hard-005` multi-hop Helios/Solstice: BM25 support recall remains 1/3 at K5, Dense reaches only 2/3 at K5. Both rank stale evidence, and neither retrieves the complete chain.
- `kbv2-hard-010` temporal Borealis: BM25 ranked `kbv2-doc-borealis-stale` at K1 and found current at K3; Dense ranked `kbv2-doc-borealis-current` at K1 but included stale by K3.
- `kbv2-hard-002` contradiction: BM25 recovered all support at K3 without the labeled contradiction, but included it at K5; Dense exposed the labeled contradiction by K3 while missing one supporting document even at K5.
- `kbv2-hard-006` contradiction: Both recovered complete support by K3, but Dense simultaneously retrieved the labeled conflicting `kbv2-doc-meridian-pending`, unlike BM25 by K5.

#### Partial visible Hybrid RRF outputs — no global aggregates

- `kbv2-hard-001` support Recall K1/3/5: 1/3, 1/3, 1; distractor appears by K3, stale appears by K3.
- `kbv2-hard-002`: 1/2, 1/2, 1; labeled contradiction appears by K3.
- `kbv2-hard-003`: unanswerable; nonempty returned results, no answer evaluated.
- `kbv2-hard-004`: ambiguous/unanswerable; candidate coverage K1/3/5: 1/2, 1, 1.
- `kbv2-hard-005`: 0, 1/3, 1/3; stale evidence is retrieved at K1.
- **Hybrid tasks `kbv2-hard-006`–`010` and the aggregate output are missing.** Do not extrapolate the Hybrid mean from only these five rows.

### Preliminary scientific interpretation

Increasing K can recover more gold support while increasing exposure to misleading documents. Dense's 0.8611 mean support recall at K5 is above BM25's 0.7778, but neither achieves complete evidence retrieval on the hardest Helios/Solstice chain; both expose labeled stale data at K5 on every task where stale risk is labeled. These are **retrieval exposure diagnostics**, not evidence that generated answers were contaminated.

**Outstanding:** capture the full Hybrid task results and printed aggregate rows for all three systems, then reconcile this manually calculated partial summary to the script's actual aggregates, archive any discrepancies and close EXP-125 only after review.

### Reproduce / capture missing tail
```bash
uv run python scripts/run_phase13_hard_robustness_comparison.py | tail -n 75
```
The full rerun must use the same source hashes. Capturing its final 75 output lines should include the remaining Hybrid rows and complete aggregate section; preserve the run's stderr/warnings separately if relevant.

## Original reproduction commands
```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_hard_robustness_comparison.py
```

## Progress
EXP-125 is **in progress**, with real-model scores and scientific closeout outstanding. EXP-124 is blocked on protocol/data/checkpoint prerequisites. Phase 13 stays at **4/6 (~67%)** completed full studies until these gates are resolved.

## Implementation validation

GitHub Actions run `43507480873`, source commit `a0882fe815673502cadf1c0defbea6001fbef03c`: **447 tests passed in 16.30s**, Ruff **All checks passed**, existing EXP-120 source-provenance, EXP-122 common representation and EXP-124 comparability audits passed. The eight new EXP-125 tests cover actual hard-v0 and Phase 9 inventory counts, all three retrieval adapters using a deterministic fake embedder, K-monotonicity, evaluator-only unanswerable treatment, source integrity, invalid rankings and conditional risk denominators. **These are not observed real MiniLM risk or recall scores.**
