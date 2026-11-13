# EXP-125 — Hard Knowledge Retrieval Robustness: Final Measured Results

## Status

**COMPLETE as a controlled, retrospective, retrieval-only robustness study on existing development tasks.** This does **not** establish safe abstention, prompt-injection resistance, generalization to new source families, or downstream answer correctness. The previously archived partial stdout has been superseded by the full user-observed second run, including the three-method aggregate section.

## Experiment contract and provenance

- Real user run: `uv run python scripts/run_phase13_hard_robustness_comparison.py`, with the complete Hybrid RRF tail and final aggregates supplied in a subsequent `tail -n 75 /tmp/exp125.log`.
- **22** frozen KnowledgeBench hard-v0 documents; **10** previously inspected tasks, **6 answerable and 4 unanswerable**, of which **2** have ambiguity candidates.
- Three fixed retrievers over the **same corpus and question strings**: `BM25Retriever`, Dense `sentence-transformers/all-MiniLM-L6-v2`, and Hybrid Reciprocal Rank Fusion with `rrf_k=60`. K = **1, 3, 5**.
- Four existing Phase 9 clean/injected prompt pairs are counted for *inventory only*. Neither paired answer-generation inference nor successful injection/mitigation was evaluated.
- The MiniLM checkpoint (103 weight objects) loaded. The HF Hub unauthenticated warning was nonfatal.
- Gold support, stale, contradiction, distractor and ambiguity labels were only used in evaluation; retrieval did not receive gold labels.

### Frozen input SHA-256

| Input | SHA-256 |
|---|---|
| `data/processed/knowledgebench_v2_hard_documents_v0.json` | `9015e8924fffcb461a7278c24e7f108d7a33377fcb6967d0f7bf0539fe9022be` |
| `data/processed/knowledgebench_v2_hard_tasks_v0.json` | `3c61ed176940a81a63ac74f42f3734aaeedac46c2c0268bf487a7e290119ea6e` |
| `data/processed/phase9_prompt_injection_pairs_v0.json` | `8cedd0675f37a31ca8995cea40267acd7a454852708a304e211e903abb248b21` |

## Actual aggregate retrieval measurements (user-supplied stdout)

All metrics below came from the **real pretrained-model experiment**, not unit-test mocks. Supporting recall, full completion and MRR denominators are the **six answerable tasks only**.

| Method | K | Mean support Recall | Full support tasks | MRR | Unanswerable nonempty retrieval |
|---|---:|---:|---:|---:|---:|
| BM25 | 1 | 0.4444 | 1/6 (0.1667) | 0.8333 | 4/4 (1.0000) |
| BM25 | 3 | 0.7778 | 4/6 (0.6667) | 0.9167 | 4/4 (1.0000) |
| BM25 | 5 | 0.7778 | 4/6 (0.6667) | 0.9167 | 4/4 (1.0000) |
| Dense MiniLM | 1 | 0.5000 | 2/6 (0.3333) | 0.6667 | 4/4 (1.0000) |
| Dense MiniLM | 3 | 0.7500 | 3/6 (0.5000) | 0.8333 | 4/4 (1.0000) |
| Dense MiniLM | 5 | 0.8611 | 4/6 (0.6667) | 0.8333 | 4/4 (1.0000) |
| Hybrid RRF | 1 | 0.5556 | 2/6 (0.3333) | 0.8333 | 4/4 (1.0000) |
| Hybrid RRF | 3 | 0.6944 | 3/6 (0.5000) | 0.8889 | 4/4 (1.0000) |
| Hybrid RRF | 5 | **0.8889** | **5/6 (0.8333)** | 0.8889 | 4/4 (1.0000) |

**Interpretation of K:** Hybrid wins mean evidence recall and complete evidence chains at K5 but not at K3; BM25 has the highest mean support recall at K3 (0.7778) and highest MRR at K3/5 (0.9167). These are six-task development-set differences, not estimates of population superiority or statistically established significance.

### Risk exposure, conditional on labeled risk tasks

**Important:** These fractions use the number of tasks with that specific labeled risk (distractor **n=2**, contradiction **n=2**, stale **n=3**), NOT all 10 tasks. A hit means the labeled evidence is in retrieved top-K; no answer-quality claim follows.

| Method | K | Distractor exposure | Contradiction exposure | Stale exposure |
|---|---:|---:|---:|---:|
| BM25 | 1 | 0/2 | 0/2 | 1/3 |
| BM25 | 3 | 1/2 | 0/2 | 3/3 |
| BM25 | 5 | 2/2 | 1/2 | 3/3 |
| Dense | 1 | 1/2 | 0/2 | 1/3 |
| Dense | 3 | 1/2 | 2/2 | 2/3 |
| Dense | 5 | 2/2 | 2/2 | 3/3 |
| Hybrid | 1 | 0/2 | 0/2 | 1/3 |
| Hybrid | 3 | 2/2 | 2/2 | 3/3 |
| Hybrid | 5 | 2/2 | 2/2 | 3/3 |

- The **two ambiguous/unanswerable tasks** have mean marked candidate coverage **0.5 at K1**, and **1.0 at K3 and K5**, for all three retrievers. This is retrieval of both competing interpretations, **not successful ambiguity resolution**.
- All four unanswerable tasks have **nonempty retrieval** for every method/K combination. There is no abstention decision, so **do not call this 100% failed abstention**.

## Per-task Hybrid RRF support recall / challenge diagnostics

| Task | K1 support | K3 support | K5 support | Key diagnostic |
|---|---:|---:|---:|---|
| `kbv2-hard-001` Atlas/Borealis | 1/3 | 1/3 | 3/3 | Labeled distractor and stale evidence retrieved from K3; full chain only at K5 |
| `kbv2-hard-002` Cirrus | 1/2 | 1/2 | 2/2 | Labeled contradiction retrieved at K3 |
| `kbv2-hard-003` parking permit | n/a | n/a | n/a | Unanswerable; documents retrieved, no answer/abstain attempt |
| `kbv2-hard-004` Nimbus ambiguity | n/a | n/a | n/a | Ambiguity candidates 1/2 at K1, 2/2 by K3 |
| `kbv2-hard-005` Helios/Solstice | 0/3 | 1/3 | **1/3** | Stale Solstice first at K1; complete multi-hop chain **never** recovered |
| `kbv2-hard-006` Meridian | 1/2 | 2/2 | 2/2 | Contradicting pending-version document retrieved by K3 |
| `kbv2-hard-007` Cirrus/Cumulus | 1/1 | 1/1 | 1/1 | Labeled distractor retrieved at K3 |
| `kbv2-hard-008` cafeteria menu | n/a | n/a | n/a | Unanswerable; documents retrieved, no answer/abstain attempt |
| `kbv2-hard-009` Orion ambiguity | n/a | n/a | n/a | Ambiguity candidates 1/2 at K1, 2/2 by K3 |
| `kbv2-hard-010` Borealis freshness | 1/1 | 1/1 | 1/1 | Correct current document ranked first; stale also retrieved by K3 |

The long failure trace for `kbv2-hard-005` is particularly informative. The returned Hybrid top5 documents include `kbv2-doc-solstice-stale` first, then `kbv2-doc-nimbus-analytics`, `kbv2-doc-helios-org`, `kbv2-doc-borealis-stale`, and `kbv2-doc-nimbus-session`: only **1/3** gold supporting documents. Increasing K to five doesn't fix the missing dependency.

### Three representative trade-offs

1. **More recall and more risk:** At K5, Hybrid reaches **0.8889 mean gold-support recall** and 5/6 complete chains, but also retrieves labeled distractors on 2/2, contradictions on 2/2, and stale documents on 3/3 applicable cases.
2. **Ranking recency matters:** For the single-hop current Borealis question (`kbv2-hard-010`), BM25 ranks the stale source first at K1; Dense and Hybrid rank current first. Yet all three include stale evidence by K3.
3. **More K isn't a substitute for reasoning:** On `kbv2-hard-005`, Hybrid and BM25 achieve only 1/3 gold supporting documents even at K5, while Dense achieves 2/3. Plain retrieval saturation hides the unresolved multi-hop dependency.

## Scope, uncertainties and rejection criteria

**Supported conclusions:** This benchmark reveals an observable retrieval quality/risk trade-off and query-dependent ranking differences. Full gold-evidence coverage and exposure metrics are auditable with precise conditional denominators. The source artifacts and retrieval interfaces were fixed for the three arms.

**Not supported:** Any result on generated answers, safe abstention, whether a retrieved contradiction caused a wrong claim, attack resistance or failure on the Phase 9 injection pairs, time/compute savings, fresh independent-family generalization, or SFT/RL superiority. These **ten previously inspected, related development tasks** do not justify confidence intervals claiming population certainty. No new heldout sample or model training took place.

## Validation, implementation, reproduction

- GitHub Actions run `43507480873` at commit `a0882fe815673502cadf1c0defbea6001fbef03c`: **447 tests passed in 16.30s**, Ruff clean, all existing provenance audit steps passed.
- `knowledgebench/evaluation/phase13_hard_robustness.py`: conditional exposure/report scoring; `scripts/run_phase13_hard_robustness_comparison.py`: real-model driver; `tests/test_phase13_hard_robustness.py`: source integrity, risk denominators, fake-encoder interfaces and fail-closed invariants.
- Exact source hashes shown above are from **the user-observed real MiniLM experiment**.

```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_hard_robustness_comparison.py
```

## Decision and campaign status

**EXP-125 closes as a fully measured retrieval-robustness DEVELOPMENT experiment.** The prompt-injection and abstention questions remain **explicitly unmeasured** and must not be presented as completed attack or abstention benchmarks. Build a downstream, source-aware verification/abstention controller with matched answer-generation and paired clean/injected tests before making safety-related claims.

**EXP-120, 121, 122, 123 and 125 are now complete (5/6 = ~83%). EXP-124 remains blocked at its actual learned-policy comparability gate** because SFT/RL action, retrieval, STOP, heldout-family and checkpoint protocols differ. The Phase 13 final review is an additional uncompleted deliverable; it is not counted as one of the six experiments.
