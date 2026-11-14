# Agentic Knowledge Lab

A research-engineering project exploring agent-native information architectures, adaptive retrieval, model training for search/tool use, and adversarial evaluation of knowledge-seeking agents.

## Projects

### 1. Agent-Native Knowledge Engine
We will build and compare:
- lexical retrieval
- dense/vector retrieval
- hybrid retrieval
- reranking
- agentic multi-step search
- hierarchical and graph-based knowledge representations
- learned retrieval policies
- fine-tuning and reinforcement-learning experiments

### 2. KnowledgeBench
We will build difficult evaluations for:
- multi-hop retrieval
- stale and contradictory evidence
- distractors
- entity ambiguity
- unanswerable questions
- search-loop failures
- prompt-injection documents

## Current status

**Phases 0–12: foundational milestones complete. Phase 13: research campaign archived and final review complete (2026-11-14).** Five scoped Phase 13 audits/experiments were completed; EXP-124 stopped as scientifically inconclusive because compatible SFT/RL checkpoints and independent evaluation families were unavailable. This is **not** a six-for-six measured research success. Phase 14 has begun: a CPU-only BM25 evidence pipeline, rule-planner fallback, traceable JSON CLI, source metadata flags, and regression tests have been implemented. Verified answers, abstention, end-to-end model evaluations, and a web UI are not yet implemented.

Start with:
- `docs/00-project-overview.md`
- `docs/01-glossary.md`
- `docs/02-learning-roadmap.md`
- `docs/03-cloud-development-setup.md`
- `docs/research/phase13-final-review.md` — final measured findings, negative results, limitations and portfolio-ready description
- `docs/research/phase13-campaign-plan.md` — experiment ledger and source protocols
- `docs/experiments/EXP-124-learned-policy-comparison-result.md` — blocked/inconclusive learned-policy experiment
- `docs/experiments/EXP-125-hard-robustness-result.md` — retrieval robustness findings

**Data integrity:** Experimental metrics must come from observed runs. The separate `EXP-124-illustrative-hypothetical-simulation-NOT-RESULTS.md` is fictional teaching material and must never be quoted as empirical performance.

## Phase 14 — evidence-first demo

The initial integration stage provides an inspectable retrieval trace **without claiming verified answers**.

```bash
uv run python scripts/run_phase14_integrated_demo.py --strategy static --top-k 3
uv run python scripts/run_phase14_integrated_demo.py --strategy auto --question "Where do exhausted failed jobs go?"
uv run pytest tests/test_phase14_integrated_pipeline.py
```

Outputs include source IDs, source metadata, search queries and fallback reasons. The `answer` field is **always `null`**, and `status` is `evidence_only_unverified`, until a separately tested answer verifier is added. An unknown planner intent triggers unchanged-question BM25 retrieval rather than leaving the result empty.

Architecture and milestone gates: [Phase 14 HLD](docs/architecture/phase14-hld.md).

## Core principle

We do not add complexity because it looks impressive.

Every component must answer:
1. What problem does it solve?
2. What is the simplest baseline?
3. How will we measure whether it helps?
4. What trade-offs does it introduce?
