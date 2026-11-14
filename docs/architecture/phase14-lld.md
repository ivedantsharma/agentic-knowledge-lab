# Phase 14 — Integrated Knowledge System LLD

## Implementation state (2026-11-14)

This is the **implemented** low-level design for a CPU-only, development-stage retrieval/verification demonstration, not a specification for a finished general knowledge assistant. Follow `docs/architecture/phase14-hld.md` for the architecture and `docs/research/phase14-integrated-development-benchmark-result.md` for measured limits.

## Source structure and interfaces

| File | Entry point | Behavior |
|---|---|---|
| `knowledge_engine/integrated/pipeline.py` | `IntegratedKnowledgeEngine(documents).query(question, strategy, top_k, max_planner_searches)` | BM25 retrieval, optional rule planner, fallback, source provenance |
| `knowledge_engine/integrated/verification.py` | `extract_source_answer(result)` | Narrow source-matched extractive candidates or explicit abstention |
| `knowledge_engine/integrated/html_report.py` | `render_demo_html(result, verdict)` | HTML-escaped, standalone trace and evidence display |
| `scripts/run_phase14_integrated_demo.py` | `main()`, `build_engine()` | Structured JSON CLI |
| `scripts/run_phase14_html_demo.py` | `main()` | Standalone HTML report export |
| `scripts/run_phase14_integrated_benchmark.py` | `evaluate_development_tasks()`, `summarize()` | Gold-after-inference evaluation of ten existing hard tasks |

### Retrieval pipeline

Construction validates nonempty unique document IDs. It builds `BM25Retriever` over exact document texts, retains `KnowledgeBenchV2Document` objects with `source_type` and optional `effective_at`, and never uses gold support IDs in retrieval.

`strategy=static` performs one unchanged-question BM25 query.

`strategy=auto` / `planner` invokes the existing `RuleBasedPlanner.next_action(PlannerState)`, searches using BM25 Top-K for each generated query, feeds only the top-ranked retrieved document's actual text through `parse_retrieval_observation`, then repeats until STOP or max three searches. Unsupported query patterns, missing hits and search-budget exhaustion trigger a **separate unchanged-question BM25 fallback**. Search steps preserve exact query and ranked document IDs; evidence is deduplicated in first-seen order.

The result has `status=evidence_only_unverified`, `answer=None`, optional `fallback_reason`, `planner_stopped`, full search traces and `EvidenceHit` objects.

**Important:** `status=evidence_only_unverified` remains in the base pipeline even when an optional extractive verdict is requested. The baseline path does not run a language model.

### Verification gate

`extract_source_answer` examines only retrieved `EvidenceHit` text and provenance. The four supported direct intents are backup cadence, job retries, validated session cache duration and signing-key rotation. It requires an explicitly named production service in the user question and matching pattern in a retrieved `service_manual` text. It rejects previous revision and pending policy sources; if two qualifying current sources contain different normalized answers it abstains.

The function returns `SourceAnswer(status, answer, citation_document_ids, reason)`. An accepted status is `source_supported_extractive`, not independently verified. Unsupported intents, absent support or contradictory current-source values yield `status=abstain`, `answer=None`. The extractor does not infer hidden service relationships, disambiguate arbitrary names, or run external source verification.

### HTML rendering and safety

`html_report.py` uses Python `html.escape` for user question, document title, document text, source IDs, extracted value, planner steps and status strings. It generates a portable, responsive, static HTML page without JavaScript or network assets; untrusted document text is displayed as *text*, not executable markup. This is output rendering isolation, not comprehensive prompt-injection resistance.

### Evaluation contract

`run_phase14_integrated_benchmark.py` loads the existing ten KnowledgeBench hard tasks after constructing the engine. The runner calls retrieval/extraction first; only then does the evaluator access `task.supporting_document_ids`, `task.expected_answer` and `task.should_answer` for scoring. It computes retrieval support recall, complete-chain fraction, extractive answer correctness on six answerable questions, abstention on four unanswerable questions, search calls, unique documents and fallback rate.

`static`: one Top3 call. `auto`: up to three Top3 planner calls **plus one fallback**. These are not cost-matched; compare descriptive outcomes only. The dataset is known development data.

## Validation observations

GitHub Actions runs with the current project integration recorded **478 passing tests** before HTML addition, Ruff clean, and a passing integrated CPU-only benchmark. Actual static extractive correctness on answerable questions was **2/6**, auto **2/6**; both abstained on **4/4 unanswerable**; the auto planner fallback rate was **10/10**, strongly limiting any claim of successful autonomous planning.

Run `uv run pytest` and `uv run ruff check .` to revalidate current source. CI also publishes a static HTML demo as `phase14-evidence-demo` artifact.

## Current known gaps

- Regex-based, service-specific extractor has poor coverage; not a general grounded answer generator
- The Phase 4 rule planner is poorly aligned with the hard-v0 corpus; all ten auto attempts fall back
- Retrieval risk flags use `source_type` only; they can miss mislabeled or adversarially edited document contents
- No explicit trusted-source registry, authority model, independent fact checking, calibrated uncertainty or model-based citation verifier
- No new source-family split, production-scale corpus, deployment, user auth, latency/cost study or matched generator evaluation
- No valid EXP-124 SFT-versus-RL comparison; those historical policies remain incompatible

## Change-control invariants

1. Never pass benchmark gold into `IntegratedKnowledgeEngine` or extractive verifier.
2. Never promote a planner extraction to a final answer without an evidence validation gate.
3. Never silently drop original-question fallback for unsupported intents.
4. Always preserve returned evidence provenance and explicit search budgets.
5. Do not claim HTML escaping validates model prompt-injection resilience.
6. Do not claim 4/4 unanswerable abstention on four inspected examples proves calibrated safety.
7. Keep unsupported experimental numerical examples isolated and labeled fictional.

## Reproduction

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_phase14_integrated_demo.py --strategy static --top-k 5 --extractive-answer
uv run python scripts/run_phase14_integrated_benchmark.py
uv run python scripts/run_phase14_html_demo.py --output phase14_demo.html
```
