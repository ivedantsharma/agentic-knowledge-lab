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

Learn:
- rewards, trajectories, credit assignment, and discounting
- on-policy stochastic exploration and action masking
- REINFORCE / policy-gradient optimization with baselines
- multi-seed variance, evaluator-only gold labels, and leakage controls
- evidence-family-disjoint evaluation and retriever-protocol confounds
- strong fixed-policy and gold-aware oracle comparisons

Deliverables:
- deterministic Reward v1/v2 retrieval environment and termination audits
- discounted returns and finite-horizon oracle / fixed baselines
- stochastic exploration and reproducible rollouts
- five-seed tabular REINFORCE training pipeline
- source-family-disjoint transfer audit and SFT-vs-RL compatibility audit
- Phase 12 architecture HLD, evaluation guardrails ADR, failure taxonomy, and final review

Status: Complete (foundational milestones met; heldout generalization remains unverified).

## Phase 13 — Full Research Campaign

Learn:
- preregistered research questions, hypotheses, controls, and ablations
- reproducible benchmark versions, provenance, and experimental manifests
- multiple independent trials, confidence intervals, and across-seed variance
- fair architecture and retriever comparisons under a shared task protocol
- failure taxonomies, stress tests, and cost/quality trade-offs
- evaluation leakage prevention and unseen evidence-family construction

Deliverables:
- Phase 13 HLD and research campaign experiment matrix
- benchmark, evaluation, and reproducibility protocol inventory
- frozen baseline configurations, seeds, and dataset split manifests
- controlled architecture ablations and multi-trial result records
- confidence/variance reporting and per-family error analysis
- decision ADRs, experiment records, and Phase 13 final review

Status: Concluded (5/6 experiments complete; SFT-vs-RL comparison blocked on missing checkpoints and unseen test families).

## Phase 14 — Final Research System & Portfolio

Learn:
- end-to-end system integration and unified retrieval adapters
- rule-based fallback routing and source provenance tracking
- extractive answer generation and calibrated abstention
- production packaging, CLI/JSON/HTML demo interfaces, and runbooks
- technical research reporting and evidence-backed portfolio framing

Deliverables:
- integrated knowledge engine
- final KnowledgeBench and benchmark/evaluation harness
- technical research report with reproduced evidence and failure cases
- architecture documentation, HLD/LLD, ADR trail, and runbook
- polished GitHub repository with reproducible experiments
- portfolio narrative with strictly supported quantitative claims

Status: Prototype delivered (integration CI passing; full system validation and hosted deployment open).
