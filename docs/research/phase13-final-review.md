# Phase 13 — Research Campaign Final Review

**Date:** 2026-11-14  
**Disposition:** **RESEARCH CAMPAIGN ARCHIVED / DOCUMENTATION COMPLETE WITH EXPLICIT UNRESOLVED SCIENTIFIC GATE.** Five studies completed within their scoped development protocols; one learned-policy study stopped as blocked/inconclusive. This is **NOT** six empirically completed studies, nor a demonstrated SFT-versus-RL generalization result.

## 1. Executive summary

Phase 13 turned a multi-retriever and agentic-knowledge prototype into a reproducible *development-stage research record*. It examined source provenance; fixed lexical, embedding and fused retrieval; claim-graph/flat/hierarchical system comparisons; query-planning behavior; learned-policy evaluation feasibility; and robustness to stale, contradictory and distracting evidence.

**Primary conclusion:** advanced retrieval/control architectures do not automatically outperform simpler baselines. Structured claim-graph traversal can recover complete evidence paths on familiar graph-specific questions, but it was tested with graph-favorable tasks and different ranking machinery. Multi-step planning can repair some multi-hop failures, but the original template-based rule planner fails outright on an unfamiliar intent. Hybrid fusion improves some top-K evidence recall scores yet broadens exposure to misleading documents. Existing SFT and RL systems cannot be ranked fairly without retraining against a common action/state/reward protocol and testing independent source families.

The campaign was **administratively closed at the request to stop compute work** after the user's Codespace became unavailable due to billing. We preserve missing measurements as missing. A separate optional illustrative EXP-124 table contains explicitly invented numbers; it is **never part of experimental evidence**.

## 2. Study ledger: what actually happened

| Study | Disposition | Source size | Verifiable result | Major limitation |
|---|---|---|---|---|
| EXP-120 provenance inventory | **Complete (audit)** | Existing source registry | Source hashes, family/task inventory and benchmark compatibility tracked | Not a model accuracy experiment |
| EXP-121 fixed BM25/Dense/Hybrid | **Complete (measured)** | 22 docs, 12 tasks, 6 exposed families | Recall@3 1.0000 for all three; MRR@3 BM25 0.8194, Dense 0.7778, Hybrid 0.8333; Hybrid−BM25 +0.0139 with family bootstrap interval [−0.1111, +0.1250] | Small, inspected families and uncertain marginal fusion effect |
| EXP-122 flat/hierarchy/graph | **Complete (system comparison)** | 4 graph-derived questions, 15 evidence atoms | Gold claim coverage: BM25 0.6250, hierarchy 0.7500, graph 1.0000; fully covered tasks 1/4, 2/4, 4/4 | Graph-derived questions, different ranking and QA capabilities; not a pure representation-only ablation |
| EXP-123 static vs rule-agent | **Complete (measured)** | 19 docs, 5 exposed tasks | Top3 Recall 0.8000; Top9 1.0000; rule agent 0.8000 with a before-first-search OOD failure in 1/5 | Unequal tool-call/context budgets, one intent OOD sample, no matched answer generator |
| EXP-124 learned SFT vs RL | **STOPPED / BLOCKED / INCONCLUSIVE** | 12 exposed routing questions for fixed-policy mechanics | Common BM25 action/observation/STOP runtime validated; fixed K3 reward +2.6000 and full evidence on exposed questions | No retrained compatible SFT/RL checkpoints, independent new-family data, matched inference or learned-policy result |
| EXP-125 hard retrieval robustness | **Complete (retrieval-only measured)** | 22 docs, 10 tasks (6 answerable) | Recall@5 BM25 0.7778, Dense 0.8611, Hybrid 0.8889; Hybrid 5/6 fully supported, but at K5 exposed labeled distractors 2/2, contradictions 2/2, stale 3/3 | No downstream answer, abstention or paired injection model test |

**Terminology:** Five **scoped experimental studies/audits are complete**, and the sixth has a documented blocked feasibility conclusion. Administrative review/archival is complete, but **the planned empirical six-study program is incomplete**.

## 3. Key findings and supported claims

### 3.1 Baseline saturation and evidence-family variance

EXP-121's common 12-task corpus saturates on Recall@3; increasing complexity cannot improve that already-maxed metric. Hybrid's MRR@3 gain of 0.0139 over BM25 has a descriptive family-level bootstrap interval that crosses zero. The correct conclusion is promising but uncertain ranking behavior, **not statistically established superiority**.

### 3.2 Representation affordance versus causal representation ablation

EXP-122 first blocked historical comparisons of unrelated Phase 5 and Phase 6 tasks, then projected source evidence into three common views. On graph-derived questions native graph QA recovered all four paths while flat and hierarchy had lower coverage. This demonstrates the system's usefulness for **relational navigation on graph-aligned tasks**, not that representation alone caused the gain or generalizes universally. Note that graph alone had native answer output; flat and hierarchy were evidence-only systems.

### 3.3 Agent planning fails differently from retrieval

EXP-123's rule agent recovered all required documents on four familiar tasks but could not construct its first query for the fifth OOD intent. This is a **planner failure before retrieval**, not a low embedding score. Static Top9 recovered all support on all five but returned more documents. Hence planning needs safe fallback, robust intent handling and stronger cost-matched baselines.

### 3.4 Learned-policy controls matter more than imagined gains

Phase 11 SFT used Hybrid K actions plus REFORMULATE. Phase 12 RL used BM25 K actions plus STOP. The old tasks, rewards, outputs and splits are incompatible. EXP-124 built an audited common BM25 `SEARCH_K1/K2/K3/K5/STOP` runtime with evaluator-hidden support, six-step limit and gamma=0.9. Real fixed K controls on 12 exposed development tasks gave discounted returns K1 +1.5333, K2 +2.3833, K3 +2.6000, K5 +2.4000. This **does not** constitute SFT/RL model comparison. The study stopped rather than claiming invented performance.

### 3.5 Better retrieval can increase exposure to bad evidence

EXP-125's Hybrid RRF at K5 retrieves 0.8889 mean support recall and 5/6 complete support, but all applicable tasks show a labeled distractor, contradiction or stale hit for each applicable risk category (2/2, 2/2, 3/3). It is important not to conflate a *retrieved risky source* with an *incorrect answer*: no answer-generation, abstention decision or injection-response test was run in EXP-125. EXP-125 is closed only for its **retrieval-only robustness** scope.

## 4. Failure taxonomy

| Failure mode | Evidence | Engineering consequence |
|---|---|---|
| Single-shot loses a multi-hop dependency | EXP-122/123 | Add evidence-chain-aware navigation or explicit decomposition, and compare to wider static retrieval |
| Handwritten intent template cannot parse a new question | EXP-123 `ood-001` | Original-query fallback and invalid-action recovery |
| Stale text ranks above current text | EXP-125 Borealis temporal task | Effective-time/source authority filters and verification |
| Contradicting facts coexist in top-K context | EXP-125 Cirrus/Meridian | Source reconciliation and conflict-aware answer generation |
| More evidence raises exposure risk | EXP-125 K1/K3/K5 | Joint retrieval quality and risk reporting; tune K on independent families |
| Fixed policy beats unstable learned RL | EXP-118 and EXP-124 gate | Keep strong fixed controls; do not promote learning on training improvement alone |
| Different learning policies solve different MDPs | EXP-119/124 | Shared state, action, reward, retriever, STOP and reproducible checkpoint contracts |
| Data families have been inspected repeatedly | All EXP-120–125 development cases | Source genuinely independent families before external-validity claims |
| Unanswerable retrieval is confused with answer abstention | EXP-125 | Run a real controller/answer generator and evaluate explicit abstention separately |

## 5. Reproducibility and evidence hygiene

- Sources and tasks: immutable SHA-256 recorded in individual EXP result files; never rename existing development cases as unseen holdout.
- Runtime: `uv`, Python 3.12 in CI, pytest and Ruff, deterministic fake-model adapter tests, plus actual pretrained MiniLM runs for relevant experiments.
- Latest observed common protocol CI: GitHub Actions run `43510455499`: **458 tests passed**, Ruff and all provenance checks passed, shared fixed-policy driver passed.
- Actual numeric results came from user-provided local runner stdout or recorded CI logs. They are separate from mocked tests.
- EXP-124 *fictional* scenario file is clearly marked **NOT RESULTS**, excluded from this ledger, excluded from all quantitative claim guidance and not cited as evidence.
- There is no full-model measured SFT-versus-RL comparison, no new untouched-family learned-policy evidence, no fair cross-system answer-generation head-to-head, no attack success rate from EXP-125, and no population-level uncertainty warranted from these inspected small samples.

## 6. Research questions answered versus left open

**Answered within limited development scope:** Can existing retrievers be compared under fixed inputs? Yes (EXP-121). Can common evidence be projected to multiple representations? Yes (EXP-122). Does graph navigation recover graph-aligned evidence chains? Yes on four existing questions. Can rule planning fail before retrieval? Yes (EXP-123). Can recall and misleading exposure rise together? Yes (EXP-125).

**Not answered:** Does SFT beat RL on a matched action/reward system? Does either beat fixed K3 on *new* families? Does retrieval evidence completeness translate into reliable answer correctness? Can the answer system consistently abstain? Can it withstand clean/injected paired documents? Do multi-step or graph systems improve real-world quality at a competitive latency/compute budget?

## 7. Portfolio-ready, evidence-grounded language

Suitable description:

> Built an agentic knowledge research laboratory with BM25, dense and hybrid retrieval, hierarchical and claim-graph search, multi-hop planning, and typed evaluation. Conducted reproducible development-scale comparisons with source-provenance audits, evidence-coverage and robustness metrics, and failure analysis; demonstrated full evidence retrieval by graph QA on four graph-aligned tasks while documenting confounds, and identified a rule-based agent's zero-search failure on an unfamiliar intent. Implemented a shared, gold-isolated BM25 control environment for future SFT/RL comparisons.

**Do not say:** “SFT/RL outperformed strong baselines,” “graph is universally better,” “hybrid safely resists injection,” “achieved calibrated abstention,” “validated on independent unseen families,” or “all six hypotheses were proven.” Only assert results with their task count and exact protocol.

## 8. Phase 14 readiness and handoff

**Ready for Phase 14 engineering/portfolio integration:** repository architecture and baseline retrieval implementations, reproducible scripts, evaluator modules, lossless evidence bridge, protocol tests, major findings, negative results, ADRs and campaign review.

**Not ready for Phase 14 research/deployment claims:** independently proven learned-agent generalization, measured final-answer correctness under matched baselines, robust refusal/abstention, source-risk mitigations validated end to end, production latency/compute performance, or independently sourced full-scale evaluation.

Prioritized next work once compute resumes: (1) integrated reproducible demo and architecture/runbook; (2) source-aware verification, uncertainty/abstention and fallback; (3) genuinely new evidence-family dataset with sealed split; (4) SFT/RL shared-protocol training/checkpointing, five-seed inference and stronger fixed controls; (5) end-to-end answer and prompt-injection paired evaluation.

These are **future tasks**, not actions that secretly occurred at campaign closeout. Any later Phase 14 README should reproduce the above caveats.

## 9. Final administrative decision

**Phase 13: review and documentation COMPLETE, research campaign ARCHIVED WITH A PARTIALLY UNRESOLVED EXPERIMENT.** Five of six scoped experiments were empirically completed or provenance-audited. EXP-124 is *closed for now as stopped/inconclusive*, not a sixth learned-policy success or measured generalization experiment. No fabricated outcomes were used. The phase may be treated as **operationally concluded** to allow portfolio work or Phase 14 engineering, with explicit unresolved claims and re-opening criteria.

Relevant records:
- `docs/research/phase13-campaign-plan.md`
- `docs/experiments/EXP-120-campaign-inventory-result.md`
- `docs/experiments/EXP-121-fixed-retriever-comparison-result.md`
- `docs/experiments/EXP-122-knowledge-representation-ablation-result.md`
- `docs/experiments/EXP-123-static-vs-agentic-search-result.md`
- `docs/experiments/EXP-124-learned-policy-comparison-result.md`
- `docs/experiments/EXP-125-hard-robustness-result.md`
- `docs/architecture/ADR-018-representation-ablation-evidence-parity.md`
- `docs/architecture/ADR-019-agentic-search-fallback-and-ood.md`
- `docs/architecture/ADR-020-retrieval-coverage-versus-evidence-risk.md`
- `docs/experiments/EXP-124-illustrative-hypothetical-simulation-NOT-RESULTS.md` (fiction only).
