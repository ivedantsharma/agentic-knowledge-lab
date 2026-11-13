# EXP-123 — Static versus Multi-Step Search: Final Measured Result

## Status
**COMPLETE as a paired, development-scale evaluation of evidence retrieval.** The observed result does **not** establish a universal or budget-matched agentic advantage.

## Source, reproducibility and protocol
Actual user execution: `uv run python scripts/run_phase13_static_agentic_comparison.py`. The original corpus contains **19 documents**, and the experiment evaluates **five** existing Phase 4 multi-hop tasks (four familiar patterns, one out-of-distribution intent). All arms use the identical `DenseSearchTool` with frozen `sentence-transformers/all-MiniLM-L6-v2` embeddings. The model loaded its 103 weight objects successfully; an unauthenticated Hugging Face Hub warning did not stop evaluation.

| File | Observed SHA-256 |
|---|---|
| `data/processed/phase4_ood_corpus_v0.jsonl` | `e94bbb4f71cbb7c39393d57611d25af9e9331dcfb05cc76c05a58f14d064ec2e` |
| `data/processed/phase4_planner_benchmark_v0.json` | `8e75b9faffbf5017c3c16905405dee7ea0bbc161cfe6090c173548b584a1da74` |

Registered arms:
1. `static_top3`: original query, 1 search call returning top 3.
2. `static_top9`: original query, 1 call returning top 9 (same *maximum result-exposure slots* as 3 calls × 3, NOT the same inference/compute budget).
3. `static_repeat3`: original query three times, top 3 each (same maximum call count, deliberately noncompetitive repeated-query diagnostic).
4. `rule_agent3`: existing `RuleBasedPlanner`, at most 3 dependent top-3 searches. Only the top-ranked document's text becomes its next-step observation; the evaluator counts *all returned documents* consistently for all arms.

Only evidence retrieval is compared; there is no matched final answer generator.

## Measured aggregate results

| Method | Mean gold-document Recall | Full gold-evidence fraction | Mean search calls | Mean unique docs | Mean hits returned | Mean repeated queries | Planner failure | Stopped |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `static_top3` | **0.8000** | **0.6000** | 1.0000 | 3.0000 | 3.0000 | 0.0000 | 0.0000 | 0.0000 |
| `static_top9` | **1.0000** | **1.0000** | 1.0000 | 9.0000 | 9.0000 | 0.0000 | 0.0000 | 0.0000 |
| `static_repeat3` | **0.8000** | **0.6000** | 3.0000 | 3.0000 | 9.0000 | 2.0000 | 0.0000 | 0.0000 |
| `rule_agent3` | **0.8000** | **0.8000** | 2.0000 | 4.6000 | 6.0000 | 0.0000 | **0.2000** | **0.8000** |

## Per-task retrieval coverage and completeness

| Task | Gold hops | Top3 Recall | Top9 Recall | Repeat3 Recall | Agent Recall | Top3 / Top9 / Repeat3 / Agent full evidence |
|---|---:|---:|---:|---:|---:|---|
| `mh-001` (Atlas backup) | 3 | 0.3333 | 1.0000 | 0.3333 | 1.0000 | No / Yes / No / Yes |
| `mh-002` (Cirrus retry) | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Yes / Yes / Yes / Yes |
| `mh-003` (Helios cache) | 3 | 0.6667 | 1.0000 | 0.6667 | 1.0000 | No / Yes / No / Yes |
| `mh-004` (Meridian signing) | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Yes / Yes / Yes / Yes |
| `ood-001` (Cirrus dead-letter destination) | 2 | 1.0000 | 1.0000 | 1.0000 | **0.0000** | Yes / Yes / Yes / **No** |

### Rule-agent observed traces

| Task | Search calls | Queried dependent chain | Top-1 observed documents | Unique retrieved IDs | Stop / error |
|---|---:|---|---|---:|---|
| `mh-001` | 3 | Atlas operator → Platform Reliability storage → Borealis backup cadence | `org_atlas` → `org_platform_reliability` → `manual_borealis` | 8 | Stopped, no error |
| `mh-002` | 2 | Developer Productivity worker → production Cirrus retries | `org_dev_productivity` → `manual_cirrus` | 5 | Stopped, no error |
| `mh-003` | 3 | Helios operator → Identity Foundations cache → Solstice duration | `org_helios` → `org_identity_foundations` → `manual_solstice` | 7 | Stopped, no error |
| `mh-004` | 2 | Security Platform signing service → Meridian rotation | `org_security_platform` → `manual_meridian` | 3 | Stopped, no error |
| `ood-001` | **0** | **No query generated** | **None** | 0 | **Planner failure before first search** |

For `mh-001`, static top3 returned `distractor_atlas_backup`, `org_atlas`, `org_platform_reliability_legacy` and retrieved only one of the three required gold documents. The agent changed its query after viewing each first hit, recovered all three required documents with three calls; one-shot top9 also recovered all three by increasing context exposure.

For `mh-003`, static top3 omitted `org_helios` (retrieved 2/3 required docs), while the agent's staged queries returned `org_helios`, `org_identity_foundations` and `manual_solstice`.

For `ood-001`, the original question concerned where exhausted Cirrus retries send failed jobs. The fixed planner's initial-query template did not recognize the dead-letter intent; it raised a planner error before issuing a search. **All three static controls recovered full evidence on that same question.** This is a decisive *demonstrated failure case* for the rule-based planner, though not a population-level failure probability.

## Interpretation and decision

- Relative to static top3: agent **increased full-evidence completion from 3/5 to 4/5** but required twice as many calls on average (2 vs 1), and its **mean Recall remained identical, 0.8000**, because the complete failure on `ood-001` offset familiar-task gains.
- Relative to static top9: agent is **worse** on both Recall and evidence completion (0.8000 vs 1.0000; 4/5 vs 5/5) but exposes fewer results (mean 4.6 unique vs 9). This is a possible quality/context *trade-off*, NOT a proven cost win because query-model calls differ and time/compute was not measured.
- Static repeat3 adds no new unique evidence and produces two repeated queries per task. It is a weak control; do not interpret its poor performance as a win against a competitive three-query static optimizer.
- The RuleBasedPlanner was engineered around Phase 4 patterns, and these old examples were previously inspected. OOD intent is a useful negative control, **not** an independent family-disjoint heldout sample.
- Because there are only five tasks with shared source families, no meaningful confidence interval or universal generalization claim is warranted.
- No answer-generator parity, independent model seeds, actual wall-clock latency, or final-answer correctness comparison was performed.

**Decision:** Close EXP-123 as a reproducible **mixed/negative** agentic-search finding. Multi-hop query adaptation can help some familiar chains but does not reliably dominate stronger context-exposure baselines and can fail on novel question intent. Do not invest in planner complexity solely on favorable familiar-task examples. Future planners should have a justified fallback to a safe original-question search, with failures evaluated on truly new intents/families, and should be compared against stronger adaptive and cost-matched controls.

## Code and validation

- `knowledgebench/evaluation/phase13_static_agentic_comparison.py`: shared retrieval interface, four-arm traces, evaluator-only gold scoring.
- `scripts/run_phase13_static_agentic_comparison.py`: frozen-MiniLM five-task driver.
- `tests/test_phase13_static_agentic_comparison.py`: protocol and fake-tool tests.
- GitHub Actions run `43503795790`, commit `0c72dad28a606f26bfd95d0d72bb1d687ff93a85`: **432 tests passed in 20.73s**, Ruff passed, source-provenance audits passed.
- All numeric outcomes in this record are **directly supplied from the user's actual pretrained-model script stdout**, not inferred from fake-tool CI tests.

## Reproduce

```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_static_agentic_comparison.py
```

## Next
EXP-124 should begin with an explicit **SFT/RL common-action, retriever-state, reward/stop, and dataset-split compatibility feasibility gate**. Existing Phase 11 and 12 policies cannot be compared head-to-head without new family-disjoint evidence and a common protocol. See Phase 12 ADR-016 and EXP-119.
