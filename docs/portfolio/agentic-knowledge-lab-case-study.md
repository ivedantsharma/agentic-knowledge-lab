# Agentic Knowledge Lab — Research Engineering Portfolio Case Study

## One-sentence summary
Built a research-oriented knowledge retrieval and evaluation framework covering lexical, dense and hybrid retrieval, multi-hop planning, hierarchical and claim-graph representations, benchmark graders, controlled experiments, and a CPU-runnable evidence trace/citation prototype.

## The technical problem
A knowledge agent must retrieve the *right* evidence from documents, decide when additional searches help, distinguish current from stale or conflicting sources, and avoid producing unsupported answers. A stronger LLM does not automatically fix missing evidence or misaligned evaluation protocols.

## Implemented system

- Existing research modules: BM25, MiniLM embeddings, Hybrid RRF, cross-encoder reranking, coarse-to-fine hierarchy, claim graph and typed evidence-grounding/agent-trace graders.
- Phase 14 integration: a common `RankingBackend` interface for BM25, Dense MiniLM and Hybrid RRF; a legacy rule-based planning loop; original-query static fallback for unsupported planner intents; source-trace JSON, citations, effective-time and source type metadata, and risk flags for previous/pending revisions.
- Narrow source-grounded output: an optional deterministic extractor returns a direct service fact with source IDs *only* if recognized question and source patterns match unambiguously; otherwise it abstains. It is not a general grounded answer generator.
- A self-contained HTML evidence demo is produced in GitHub Actions as an artifact. All untrusted document strings are HTML-escaped before display.
- Existing KnowledgeBench hard tasks are integrated for diagnostic evidence recall, source-answer agreement, abstention and trace/fallback metrics.

## Selected real measurements (all small, previously inspected development evaluations)

| Study | Evidence-backed finding | Scope caveat |
|---|---|---|
| EXP-121 | Hybrid MRR@3 0.8333 vs BM25 0.8194; family-bootstrap diff interval spans zero | 12 inspected tasks / 6 families |
| EXP-122 | Graph evidence coverage 1.0000 vs flat 0.6250 and hierarchy 0.7500 | Four graph-aligned tasks, different rankers; not a causal graph-only win |
| EXP-123 | Rule agent fully recovered evidence on 4/5 tasks but failed before searching on the unfamiliar fifth; static top9 recovered 5/5 | Call/context budgets not matched, no matched answer generator |
| EXP-124 | Common BM25 policy runtime implemented; fixed K3 developmental return +2.6000; learned SFT/RL comparison stopped inconclusive | Incompatible historical policies and no fresh independent source families |
| EXP-125 | Hybrid Recall@5 0.8889, full evidence on 5/6 answerable tasks, with extensive labeled stale/contradiction/distractor exposure | Retrieval-only; no generated answer/abstention or attack success measured |
| Phase 14 diagnostic | Static support recall 0.7778, auto 0.8889; extractive answers correct 2/6 answerable tasks, abstained 4/4 unanswerable; auto fell back 10/10 times | Ten inspected tasks, unequal call budgets, narrow template extractor |

These metrics are **not** general production performance claims. All user-supplied real-model numbers are separated from synthetic teaching-only examples in the repository. No invented SFT-versus-RL result belongs in a resume.

## Why the failure analysis matters
- A graph-favorable benchmark cannot establish graph representation as the causal driver of better results.
- A planner can fail to form a query for a new intent, before retrieval quality even matters.
- Higher K can retrieve correct evidence and dangerous/conflicting context together.
- An extractor that abstains on four of six answerable development questions has low answer coverage, even if it abstains on four of four labeled-unanswerable questions.
- A model trained to classify one-step Hybrid K/REFORMULATE actions cannot be compared fairly with a sequential RL STOP/BM25 controller without retraining and common states/rewards.
- The new Phase 14 fallback prevents a rule-unsupported query from returning an empty trace, but the auto planner's **10/10 fallback rate** shows that flexible planning is still unsolved.

## Engineering decisions
- Explicit per-source provenance is a first-class field, not an afterthought.
- Safeguard planning with unchanged-question fallback.
- Separate retrieval success, source-supported extraction, abstention, risk exposure, and final generated-answer correctness; do not collapse them into one score.
- Treat gold support/expected-answer data as evaluator-only.
- Keep BM25 CPU-only path and CI demo runnable without a GPU or Codespaces.
- Favor reproducibility and negative findings over an artificially impressive research story.

## Demonstration
Start in the repository README, or use `scripts/run_phase14_integrated_demo.py` for JSON traces and `scripts/run_phase14_html_demo.py` for an HTML walkthrough. GitHub Actions uploads a `phase14-evidence-demo` artifact on successful CI runs.

The HTML demo isn't a hosted application; it's a portable report showing the actual engine outputs.

## What remains unproven
Reliable adaptive planner success on novel question forms; world-truth verification of citations; robust temporal/contradiction resolution; calibrated abstention; resistance to prompt injection by an LLM; fresh independent-family generalization; matched answer quality and latency comparisons; learned SFT/RL policy superiority; production deployment.

## Honest interview narrative
> I built a benchmark-driven agentic knowledge lab with retrieval, structured knowledge representations and tool-use evaluation. I established strong BM25/Dense/Hybrid baselines, implemented graph and hierarchical comparisons, identified planner failures under unfamiliar questions, and measured a trade-off between support recall and misleading-source exposure. To make the architecture inspectable, I integrated retrieval adapters, a fallback planner, a source-aware extractive prototype and a standalone evidence-trace demo, with tests and GitHub CI. I explicitly avoided claiming learned SFT/RL generalization because the old policies had incompatible action and reward protocols and no newly independent evaluation families.

## Key references
- `docs/research/phase13-final-review.md`
- `docs/research/phase14-integrated-development-benchmark-result.md`
- `docs/architecture/phase14-hld.md`
- `docs/architecture/phase14-lld.md`
- `docs/operations/phase14-runbook.md`
