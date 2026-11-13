# Learning Roadmap

We learn only what is needed for the next engineering step.

## Phase 0 — Foundations & Environment

Learn:
- Codespaces basics
- terminal basics
- Git and GitHub basics
- Python environments
- repository structure
- basic LLM terminology
- documentation system

Deliverables:
- working cloud dev environment
- starter test passes
- CI passes
- documentation readable

Status: Complete.

## Phase 1 — Retrieval & Evaluation Foundations

Learn:
- research questions
- hypotheses
- baselines
- metrics
- experimental design
- embeddings
- cosine similarity
- BM25
- dense retrieval
- hybrid retrieval
- reciprocal rank fusion
- retrieval evaluation

Deliverables:
- BM25 baseline
- dense baseline
- hybrid RRF baseline
- typed benchmark schemas
- Recall@K, Precision@K, MRR evaluators
- controlled experiment protocol

Status: Complete.

## Phase 2 — Ingestion, Chunking & Retrieval Architecture

Learn:
- parsing
- metadata
- chunking
- overlap
- evidence provenance
- structure-aware chunking
- contextualized retrieval units
- Hit@K
- cross-encoder reranking

Deliverables:
- source-document ingestion
- fixed-size chunker
- overlap experiments
- chunk-size comparison
- evidence-derived relevance labels
- structure-aware chunks
- contextualized chunks
- Markdown ingestion
- retrieve-then-rerank pipeline

Status: Complete.

## Phase 3 — Multi-Hop Retrieval Foundations

Learn:
- dependent searches
- question decomposition
- intermediate facts
- evidence chains
- multi-document questions
- why single-hop retrieval fails

Deliverables:
- multi-hop task schema
- synthetic multi-document benchmark
- single-hop baseline
- deterministic multi-hop baseline
- evidence-chain metrics
- structured retrieval state
- failure analysis

Status: Complete.

## Phase 4 — Agentic Search Planner

Learn:
- agent loops
- planner actions
- tool calling
- planner state
- query generation
- tool selection
- stopping conditions
- planning

Deliverables:
- planner action schema
- planner state + trace
- search-tool abstraction
- oracle planner baseline
- rule-based planner baseline
- autonomous query planner
- stopping-policy evaluation

Status: Complete.

## Phase 5 — Hierarchical Retrieval

Status: Complete.

Learn:
- document → section → chunk retrieval
- coarse-to-fine search
- parent-child navigation
- hierarchical indexes

## Phase 6 — Knowledge Graph & Claim/Evidence Retrieval

Status: Complete.

Learn:
- entities
- relations
- knowledge graphs
- claim/evidence graphs
- retrieval over structure

## Phase 7 — KnowledgeBench v2: Hard Retrieval Evals

Status: Complete.

Learn:
- multi-hop tasks
- distractors
- ambiguity
- temporal/stale knowledge
- contradictions
- unanswerable questions

## Phase 8 — Agent Evaluation & Graders

Status: Complete.

Learn:
- agent traces
- tool-use metrics
- retrieval-path metrics
- deterministic graders
- model graders
- groundedness

## Phase 9 — Adversarial Robustness & Failure Analysis

Status: Complete.

Learn:
- prompt-injection documents
- search loops
- misleading evidence
- long-context distraction
- failure taxonomies

## Phase 10 — Adaptive Retrieval & Query Understanding

Status: Complete.

Learn:
- BM25 vs dense vs hybrid vs graph routing
- query classification
- adaptive top-k
- query transformation
- retrieval policies

## Phase 11 — Fine-Tuning Retrieval/Search Behavior

Status: Complete.

Learn:
- PyTorch basics
- Hugging Face Transformers
- LoRA / PEFT
- supervised fine-tuning
- retrieval-policy training data

Deliverables:
- typed retrieval-policy action space
- frozen-model policy baseline
- target-only causal-LM SFT formatting
- LoRA optimization pipeline
- measured oracle policy dataset
- evidence-family-disjoint evaluation
- class-balanced SFT baseline
- Phase 11 failure analysis and final review

## Phase 12 — RL for Retrieval Policy

Status: Complete (foundational learning milestones; no robust heldout policy generalization claim).

Learn:
- rewards, trajectories, credit assignment and discounting
- on-policy stochastic exploration and action masking
- REINFORCE / policy-gradient optimization with baselines
- multi-seed variance, evaluator-only gold labels and leakage controls
- evidence-family-disjoint evaluation and retriever-protocol confounds
- strong fixed-policy / gold-aware oracle comparisons

Deliverables:
- deterministic Reward v1/v2 retrieval environment and termination audits (EXP-111–114)
- discounted returns and finite-horizon oracle / fixed baselines (EXP-115)
- stochastic exploration and reproducible rollouts (EXP-116)
- five-seed tabular REINFORCE training, positive in-sample result (EXP-117)
- BM25 source-family-disjoint transfer audit, negative/unstable result (EXP-118)
- Phase 11 SFT versus Phase 12 RL compatibility audit (EXP-119)
- `docs/architecture/phase12-hld.md`
- `docs/architecture/ADR-016-rl-policy-evaluation-guardrails.md`
- `docs/research/phase12-failure-taxonomy.md`
- `docs/research/phase12-final-review.md`
- EXP-111–119 experimental protocols/results in `docs/experiments/`

Key result:
- EXP-117 training-task return +1.5765 → +2.6722 (five-seed mean).
- EXP-118 heldout return +1.6573 → +1.7540 with large seed variability,
  completion 0.7753 → 0.7416; fixed K3 +2.6000 / 1.0000 completion.
- No apples-to-apples Phase 11 SFT-vs-Phase 12 RL win established.
- See final review and ADR-016 before extending policy training.

## Phase 13 — Full Research Campaign

Status: Current (EXP-120, EXP-121 and EXP-122 system-level development comparison complete; EXP-123 agentic-vs-static protocol next).

Learn:
- preregistered research questions, hypotheses, controls and ablations
- reproducible benchmark versions, provenance and experimental manifests
- multiple independent trials, confidence intervals and across-seed variance
- fair architecture / retriever comparisons under the same task protocol
- failure taxonomies, stress tests, cost and quality trade-offs
- evaluation leakage prevention and new heldout evidence-family construction

Planned deliverables:
- phase13 HLD and research campaign plan / experiment matrix
- EXP-120: benchmark, evaluation and reproducibility protocol inventory (complete; 390 tests, Ruff and provenance audit passed)
- frozen baseline configurations, seeds, dataset and split manifests
- controlled architecture ablations and multi-trial result records
- strong fixed and oracle baselines alongside all learned variants
- confidence/variance reporting, per-family error analysis and negative findings
- decision ADRs, experiment records and Phase 13 final review

Gates before strong claims:
- no tuning against already inspected EXP-118 heldout families as pristine test data
- a common retriever/action/state/termination/evaluation protocol for any SFT-vs-RL comparison
- independent, genuinely unseen evidence families and separate answer-quality metrics
- no unsupported claim that RL beats fixed K3, improves final answers, or generalizes broadly

## Phase 14 — Final Research System & Portfolio

Status: Planned (not started).

Deliverables:
- integrated knowledge engine
- final KnowledgeBench and benchmark/evaluation harness
- technical research report with reproduced evidence and failure cases
- architecture documentation, HLD/LLD, ADR trail and runbook
- polished GitHub repository with reproducible experiments
- portfolio/application narrative with only supported quantitative claims
