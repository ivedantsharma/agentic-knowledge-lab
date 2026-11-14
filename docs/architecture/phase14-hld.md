# Phase 14 — Integrated System Architecture and Engineering Plan

## Status (2026-11-14)

**Phase 14.0: architecture and integration contract defined. Phase 14.1: integrated BM25/Dense/Hybrid ranking adapters with static fallback CI-validated (487 tests). Phase 14.2: narrow optional source-cited extractive gate and explicit abstention rules implemented; independent answer-quality validation remains pending.** The pipeline returns **retrieved evidence only**, not verified answers or calibrated abstentions. Phases 14.2–14.7 are NOT complete.

## Goal
Deliver a coherent runnable Agentic Knowledge Engine and KnowledgeBench demonstration whose claims remain traceable to the real Phase 13 results. Avoid implying the historical fixed template planner generalizes or that an LLM has verified evidence.

## Architecture (HLD)

```text
Question
  |
  +--> Shared ranking backend --------------------+
  |    BM25 / Dense MiniLM / Hybrid RRF            |
  |                                               |
  +--> Existing RuleBasedPlanner                  |
           |                                       |
           +--> generate query                    |
           +--> selected backend top-k evidence               |
           +--> observe top1, update state        |
           +--> STOP or query failure ------------+
                      |
          If failure/budget exhaustion:
          original-question search on same backend
                      |
           Ordered unique evidence results
           Source type/effective date provenance
           Previous/pending source-risk flags
                      |
             EVIDENCE ONLY / UNVERIFIED
             answer = null
                      |
          Future 14.2 verification + answer/abstention
          Future 14.3 KnowledgeBench integration
```

## Component contracts

**Retrieval:** common `RankingBackend` in `knowledge_engine/integrated/backends.py` can use the existing BM25, frozen Dense MiniLM or Hybrid RRF. BM25 is the no-download default. The engine indexes `KnowledgeBenchV2Document` with stable document IDs, text, source types and effective dates. This CPU-only starter does not download embeddings.

**Planner:** existing `RuleBasedPlanner.next_action(PlannerState)` and `parse_retrieval_observation`; only the first hit text is passed to the next planner step. Failed query generation or budget exhaustion triggers a static original-question query. Earlier planner failures in EXP-123 motivate this fallback.

**Provenance:** `EvidenceHit` includes original document ID, title, full text, source type, effective date and a *metadata-derived* risk flag for previous revision or pending revision. These flags do not use the benchmark's gold distractor/stale labels, and do not independently establish factual authority.

**Output:** `IntegratedResult` contains requested/used strategy, fallback reason, whether planner STOP occurred, every search query and returned document IDs, deduplicated ordered evidence, `status=evidence_only_unverified`, and `answer=null`. The planner's raw extracted answer is intentionally never returned as a verified final answer.

**CLI:** `scripts/run_phase14_integrated_demo.py` reads the existing hard-v0 corpus and prints inspectable JSON. No web service, UI, generation model or question-answer correctness claim exists yet.

**Boundaries:** input validation ensures positive top-k within corpus size, max planner steps 1–6 and nonempty unique documents; no benchmark gold, support labels or expected answers enter policy or search queries. This does not demonstrate prompt-injection resistance of a downstream language model.

## Reproduction

```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase14_integrated_demo.py --strategy static --top-k 3
uv run python scripts/run_phase14_integrated_demo.py --question "Where do failed jobs go after retries?" --strategy auto
```

The second query intentionally demonstrates a rule-planner unsupported-intent fallback. Add `--backend dense` or `--backend hybrid` to the JSON CLI to load MiniLM on demand (separate from CPU-only CI). Inspect `strategy_used`, `fallback_reason`, `steps`, and `evidence` instead of treating unverified evidence as final answer.

## Subsequent milestones and explicit exit gates

| Milestone | Exit gate | Status |
|---|---|---|
| 14.0 architecture/contract | HLD, real module import verification, evidence boundaries | **Completed as prototype architecture** |
| 14.1 retrieval integration | BM25/Dense/Hybrid common rankers, static/planner/fallback, CI tests | **Completed as integration plumbing**; broad planner effectiveness unproven |
| 14.2 answer verification/abstention | Source-aware evidence checking and real answer/abstain accuracy | **Narrow prototype only**; 2/6 answers correct on inspected tasks |
| 14.3 KnowledgeBench integration | Per-task evaluator and explicit answer/abstention/call metrics | **Development diagnostic complete**; no unseen-family validation |
| 14.4 interface/demo | JSON traces and portable source-cited HTML demo artifact | **Completed as static demo** (not a hosted web app) |
| 14.5 reproducibility | CI, runbook, regression/failure tests and production reproducibility | **Completed for CPU prototype**; production/model validation open |
| 14.6 portfolio/report | Credible README, research portfolio case study, documentation | **Completed for current evidence scope** |
| 14.7 final review/handoff | Audited supported results and remaining scientific blockers | **Review in progress** |

## Phase 13 constraints inherited

EXP-124 stopped/inconclusive; SFT and RL models were not compared on new independent source families. EXP-125's K5 hybrid recall 0.8889 was accompanied by distractor/contradiction/stale exposure. Use a verifier/abstention gate in 14.2 before any answer correctness or trust claim. The existing hard corpus is inspected development data.

## Execution environment

GitHub Actions provides a repository-native test path while Codespaces is unavailable due to billing. Documentation and source changes are made through GitHub. No one should claim an end-to-end pretrained-model run merely from CPU unit tests.

## Phase 14.2 prototype — bounded extractive source verification

`knowledge_engine/integrated/verification.py` provides an **opt-in** `extract_source_answer(result)` function with structured `SourceAnswer`. It is intentionally limited to direct service-specific backup cadence, job retries, cache duration and signing-key rotation when the service name appears **explicitly in the question** and the `service_manual` corpus text contains a matching fixed expression.

The extractor excludes `service_manual_previous_revision` and `pending_policy_revision` sources and abstains on distinct answers from multiple qualifying service manuals. Each accepted extracted answer includes citation document IDs; no benchmark gold support labels or expected answers enter this logic. The output is `source_supported_extractive` and explicitly **NOT independently fact-checked**. Multi-hop service inference, arbitrary user questions, contradiction resolution outside the narrow patterns, stale records with incorrect source metadata, malicious document text outside recognized patterns, and calibrated uncertainty are unsolved.

The original `IntegratedResult.answer` remains `null` and `status=evidence_only_unverified`; the optional CLI flag `--extractive-answer` adds a separate `source_answer` field containing a source-supported candidate or an abstention.

```bash
uv run python scripts/run_phase14_integrated_demo.py --strategy static --top-k 5 --extractive-answer
uv run pytest tests/test_phase14_source_answer.py
```

**Exit criterion for real 14.2:** run source-independent answer/abstention checks with counterfactual and misleading source tests, document false positives and false negatives, and compare to a matched generator. The current prototype does not meet the complete end-to-end reliability gate.

## Observed Phase 14 integration checkpoint

CI run `43590314766` on commit `50953715ea86faed0c5ecb53f09d9880841be7f6`: **487 tests passed in 15.28s**, Ruff clean, existing research audits passed, both evidence JSON and optional extractive CLI smoke checks passed, integrated KnowledgeBench development evaluation ran, and a self-contained `phase14-evidence-demo` HTML artifact was generated and uploaded. These CI checks cover real BM25 engine execution and fake-encoder Dense/Hybrid adapter tests; they do **not** claim real new-family Dense/Hybrid end-to-end inference outcomes.

On the known ten-task benchmark, **static extractive answer correct 2/6, auto 2/6, auto fallback 10/10**. Source-aware verification, flexible planner generalization and calibrated abstention remain unachieved.
