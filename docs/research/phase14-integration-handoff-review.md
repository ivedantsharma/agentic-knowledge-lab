# Phase 14 — Integrated Knowledge Engine: Engineering Handoff Review

**Date:** 2026-11-14  
**Disposition:** **Version 0.1 evidence-first research demo released and reproducible through GitHub Actions.** Phase 14's *engineering prototype* is packaged; general-answer verification, new-family research validation, reliable flexible planning and production-readiness remain **explicitly incomplete**. The Phase 14 research/deployment goals cannot honestly be declared entirely achieved.

## 1. What was actually delivered

**Shared ranking:** `knowledge_engine/integrated/backends.py` adapts BM25, Dense MiniLM and Hybrid RRF behind the same `rank(query, top_k)` interface. Dense/Hybrid accept an injected encoder for CI tests and can load frozen MiniLM on demand. No real new-family Dense/Hybrid end-to-end benchmark was run in Phase 14.

**Integrated search:** `knowledge_engine/integrated/pipeline.py` handles static or legacy rule-planned searches, top1 observation parsing, search traces, deduplicated document provenance and an unchanged-question fallback. A malformed backend cannot supply unknown or duplicate IDs.

**Conservative source answer prototype:** `knowledge_engine/integrated/verification.py` optionally extracts direct service facts from clearly labeled `service_manual` text; it excludes previous/pending policy revisions, rejects conflicting current answers, requires a named service in the question and abstains otherwise. This is **not** independent fact-checking or general question answering. Base evidence result `answer=None` is never silently promoted into a final answer.

**User-facing demos:** JSON CLI (`scripts/run_phase14_integrated_demo.py`) and a static, responsive HTML evidence/citation report (`scripts/run_phase14_html_demo.py`). Source and user text are HTML-escaped. Successful GitHub Actions CI runs upload `phase14-evidence-demo`; the artifact opens in a browser without Codespaces or a server.

**Measurement:** `scripts/run_phase14_integrated_benchmark.py` uses ten *previously inspected* KnowledgeBench hard tasks, gold labels exclusively in the evaluator, and reports evidence recall, correct extractive answer fraction, abstention and planner fallbacks.

**Documentation:** HLD, LLD, no-Codespace CI runbook, research development benchmark result, polished README and honest portfolio case study.

## 2. Measured results, not guesses

On the existing 22-document/10-question hard-v0 corpus (6 answerable, 4 unanswerable), the CPU-only integrated benchmark actually ran in GitHub CI:

| Metric | Static BM25 Top3 | Auto (up to three planned Top3 searches plus fallback) |
|---|---:|---:|
| Mean supporting-document recall | 0.7778 | 0.8889 |
| All supporting evidence returned | 4/6 | 4/6 |
| Answerable questions answered correctly by narrow extractor | **2/6** | **2/6** |
| Answerable questions abstained on | 4/6 | 4/6 |
| Unanswerable questions abstained on | 4/4 | 4/4 |
| Mean unique documents | 3.0 | 3.3 |
| Mean search calls | 1.0 | 1.6 |
| Fallback rate | 0/10 | **10/10** |

The different search budgets make static-versus-auto recall **descriptive only**, not a controlled agentic advantage. Universal fallback shows the old template planner is not aligned with these hard question/document patterns. The extractor has **low answer coverage** and must not be promoted as a fully grounded knowledge answer system; the 4/4 abstention on four inspected cases is not a calibrated safety claim.

Observed CI source validation: workflow run `43590314766` for integration code commit `50953715ea86faed0c5ecb53f09d9880841be7f6`, **487 passing tests**, Ruff clean, benchmark and HTML CI artifact steps successful. Subsequent documentation commits are not separate model experiments. All actual source-metric records live at `docs/research/phase14-integrated-development-benchmark-result.md`.

## 3. Goals achieved and not achieved

| Scope | Result |
|---|---|
| 14.0 Architecture / contracts | **Completed for prototype** |
| 14.1 Unified ranking/integration and fallback | **Implemented and tested** |
| 14.2 Verifier / abstention | **Narrow extractive prototype only; broad answer correctness not achieved** |
| 14.3 KnowledgeBench integration | **Development diagnostic complete; independent end-to-end evaluation open** |
| 14.4 Human-readable demonstration | **Completed as JSON plus static HTML; not a hosted service** |
| 14.5 Reproducibility | **CI/runbook completed for prototype; production validation open** |
| 14.6 Portfolio artifacts | **README, HLD/LLD and grounded case study completed** |
| 14.7 Review and handoff | **This report completes prototype handoff**, with unresolved research gates documented |

The engineering handoff/report is complete, but not every originally intended full-scale capability has been proven.

## 4. Failures and scientific limitations

- **Knowledge graph and hierarchy integration:** existing research components remain accessible as individual modules, but Phase 14's common runtime currently directly supports BM25, dense, hybrid and legacy rule planning. It does not yet expose graph QA and hierarchical search through the same adapter. Do not claim all architectures run through one unified production service.
- **Planner robustness:** EXP-123 showed a pre-search failure for unseen intent; Phase 14 adds fallback, but on its hard development benchmark the auto controller falls back **10/10** times. This prevents empty retrieval, not a solved general planner.
- **Verification/grounding:** only explicit current service-manual patterns yield answers. Other answerable cases abstain. No cross-document inference or independent truth verification.
- **Source-risk checking:** metadata flags for previous/pending revisions can be wrong or incomplete. They are not a production trust registry and cannot establish authority.
- **Abstention:** the low answer coverage and tiny inspected unanswerable set do not demonstrate calibrated refusal.
- **Prompt injection:** HTML rendering escapes markup, and the deterministic extractor ignores most unrelated directive text. These do **not** prove that a language model is resistant to injected evidence.
- **Learned control:** EXP-124 remains inconclusive; no comparable retrained SFT/RL checkpoint generalization experiment occurred.
- **Methodological limitations:** tiny previously inspected benchmarks, unequal tool-call budgets, no Phase 14 real-run independent dense/hybrid latency/cost numbers, no new-family evaluation.

## 5. Suggested next engineering milestones once compute/data allow

1. Extend the unified adapter to hierarchical and claim-graph retrieval with strict output evidence/provenance normalization.
2. Replace the fragile fixed-template planner with a tested, question-aware planner that supports unseen intents and a **same-budget** static comparison.
3. Introduce explicit source authority and time/version handling, conflict resolution, source-cited answer generation and a verified abstain decision.
4. Create independent evidence families with frozen pretraining splits, and run end-to-end answer/abstention and paired clean/injected source studies.
5. If policy learning is pursued, retrain and checkpoint SFT and RL under the EXP-124 shared action/reward protocol and compare seeds against strong fixed K baselines.
6. Add realistic latency/cost and production security/deployment tests before making any service-level claims.

These are **future needs**, not accomplishments of Phase 14.

## 6. How to inspect without Codespaces

Use GitHub Actions for the tests and HTML artifact; see `docs/operations/phase14-runbook.md`. Browser-viewable source files, benchmark results and research explanations remain available even when Codespaces billing prevents an interactive cloud environment.

Key references:
- `README.md`
- `docs/architecture/phase14-hld.md`
- `docs/architecture/phase14-lld.md`
- `docs/research/phase14-integrated-development-benchmark-result.md`
- `docs/portfolio/agentic-knowledge-lab-case-study.md`
- `docs/research/phase13-final-review.md`

## 7. Final scope statement

**Phase 14 integration-prototype and portfolio handoff: delivered. Phase 14 general research system/deployment-quality objectives: NOT yet complete.** No imaginary results, unrun trained-model metrics or unsupported safety claims were used. This is a well-instrumented **starting point for further research engineering**, not proof of a general reliable knowledge agent.
