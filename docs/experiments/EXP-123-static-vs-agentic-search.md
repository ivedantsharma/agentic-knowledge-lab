# EXP-123 — Static Retrieval versus Multi-Step Agentic Search

## Status
**Preregistered design / protocol review. No EXP-123 numerical results yet.** EXP-120–122 are complete development studies; EXP-123 is next in the Phase 13 campaign.

## Core research question

With **the same dense search tool, source corpus, multi-hop questions, and limited search budget**, does planning a sequence of dependent searches recover more gold evidence than a fixed one-shot query? How much does each additional search cost, and how reliably does the agent stop?

## Lessons inherited from earlier phases

- Phase 3 established dependent-question retrieval; Phase 4 already implements `DenseSearchTool`, `PlannerState`, typed SEARCH/STOP actions, `RuleBasedPlanner`, and `execute_task`.
- EXP-121 showed retrieval architecture can saturate on simple tasks; a multi-hop dataset is more discriminative for search *behavior*.
- EXP-122 showed source parity alone does not isolate an architectural variable: never compare unrelated task sets or pretend output candidates have equal compute cost.
- EXP-118 warned that learned training gains do not establish heldout generalization.

## Initial candidate benchmark and code (already verified)

- `data/processed/phase4_ood_corpus_v0.jsonl`
- `data/processed/phase4_planner_benchmark_v0.json`
- `knowledge_engine/agent/search_tool.py`: `DenseSearchTool.search(query, top_k)`
- `knowledge_engine/agent/rule_based_planner.py`: `RuleBasedPlanner.next_action(state)`
- `knowledge_engine/agent/state.py`: `PlannerState`
- `knowledge_engine/agent/actions.py`: `PlannerActionType.SEARCH`, `PlannerActionType.STOP`
- `knowledge_engine/agent/observation_parser.py`: parse returned text into next planner state
- `knowledge_engine/agent/evaluation.py`: Phase 4 task metrics
- `scripts/run_phase4_planner_comparison.py`: existing engine and run protocol

**Important:** The existing Phase 4 runner fetches top-three results but exposes only the first hit to the planner, and includes extra Qwen components for the historic hybrid planner. EXP-123 must explicitly decide and freeze which evidence is *visible* versus *retrieved* so the one-shot and multi-step traces are scored consistently. It must not require heavy Qwen checkpoints merely to compare a static control and deterministic rule planner.

## Initial controlled protocol (subject to feasibility validation before implementation)

| Factor | Static baseline | Multi-step search |
|---|---|---|
| Underlying search engine | Same frozen MiniLM dense `DenseSearchTool` | Exactly the same instance |
| Corpus and tasks | Identical source files and question texts | Identical |
| First search | Original question | Planner-generated query from original question |
| Subsequent search | None | Query reformulation based on visible previous top-hit observation |
| Tool call cap | 1 | Up to 3 SEARCH actions |
| Results per call | Top 3 ranked document IDs | Top 3 ranked document IDs |
| Planning stop | After first retrieval | Explicit STOP or cap |
| Gold task path | Evaluator only | Evaluator only |
| Main outcome | Coverage of required evidence docs | Same coverage definition |

**Resource reporting:** both per-call `top_k=3` and maximum number of calls must be shown. This is a *different total search budget* by design; therefore the naive agent/static comparison is not a budget-matched causal claim. Add a fair **three-call static control** (e.g., repeat/original variants fixed before seeing gold) if comparing maximum tool-call budgets. Report both total tool calls and unique documents returned. Do not treat hit at top1 as equivalent to coverage of all top3 without a declared exposure convention.

### Primary and secondary metrics

- Primary: per-task gold-document **Recall** and fraction with all required evidence retrieved, using exactly the same retrieved-ID accounting.
- Secondary: unique evidence IDs exposed, search call count, repeated queries, planner exceptions, explicit STOP vs cap exhaustion, relevance of search traces, and if **both** arms have the same answer generator, end-to-end grounded exact-answer accuracy.
- Do **not** report an answer-accuracy head-to-head when only the planner generates answers.
- Record each task's hop count, family, known/inspected status and provenance. Bootstrap over independent families, not paraphrases, if enough valid groups exist. This is primarily an existing **development** benchmark.

## Feasibility gate before claims

1. Audit Phase 4 source/task hashes, task schemas and gold chain provenance.
2. Verify `DenseSearchTool` result accounting and planner state transitions without gold leakage.
3. Freeze a reproducible shared-interface harness; test with a fake search backend and real source invariants.
4. Define the static multi-call fair control and whether answer generation can be matched at all.
5. Only then run the actual frozen MiniLM tool; record metrics and failures in `EXP-123-static-vs-agentic-search-result.md`.
6. Do not claim an agentic advantage if gains depend on extra calls, task-specific handwritten shortcuts, or inspected benchmark families.

## Reproduction status

Protocol only; no EXP-123 driver exists yet. The next engineering step is to implement the dataset/protocol feasibility audit and shared retrieval trace adapter, with tests and CI before measuring pretrained-model outcomes.


## Implemented comparison arms (fixed before numerical run)

The shared harness lives at `knowledgebench/evaluation/phase13_static_agentic_comparison.py`, the driver at `scripts/run_phase13_static_agentic_comparison.py`, and unit tests at `tests/test_phase13_static_agentic_comparison.py`.

- `static_top3`: original question, one DenseSearchTool call, expose all top 3 hits.
- `static_top9`: original question, one DenseSearchTool call, expose up to 9 hits; matches the *maximum exposure slots* of three top-3 calls, **not model computation or call count**.
- `static_repeat3`: same original question, three identical top-3 calls; matches the agent's maximum **call count** but repeats the same evidence. It is a diagnostic weak control, not an optimized static three-query system.
- `rule_agent3`: existing RuleBasedPlanner makes up to three SEARCH calls (top3 returned on each), sees only the top1 document text from each retrieval when updating PlannerState, and may STOP after the third call. The planner receives no gold hops, answers, expected document IDs or benchmark category.

For **all arms**, gold supporting-document recall is scored on the union of **all returned hit IDs**, not just the single document shown to the planner. Both top-K exposure and first-hit observation must be reported to prevent an evaluation accounting mismatch.

Important asymmetries: static_top9 can expose nine documents in one call; agent gets three candidates each across at most three differently worded calls; the planner uses task-specific regular-expression behaviors originally developed in Phase 4; the benchmark is historic/inspected. No common answer-generation capability is provided, so do not compare answer accuracy. No novel model training or fresh family-disjoint evaluation is claimed.

### Exact reproduction
```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_static_agentic_comparison.py
```

Actual numerical outputs must be archived in `EXP-123-static-vs-agentic-search-result.md` after the full model run. CI fake-backend tests establish harness integrity, not frozen-model retrieval accuracy.
