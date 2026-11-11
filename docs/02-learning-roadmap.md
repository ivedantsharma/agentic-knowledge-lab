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

Status: Current.

Learn:
- PyTorch basics
- Hugging Face Transformers
- LoRA / PEFT
- supervised fine-tuning
- retrieval-policy training data

## Phase 12 — RL for Retrieval Policy

Learn:
- rewards
- trajectories
- credit assignment
- policy optimization
- evaluation leakage risks

## Phase 13 — Full Research Campaign

Learn:
- controlled experiments
- ablations
- multiple trials
- confidence and variance
- architecture comparisons
- failure analysis

## Phase 14 — Final Research System & Portfolio

Deliverables:
- integrated knowledge engine
- final KnowledgeBench
- technical report
- architecture documentation
- polished GitHub repository
- portfolio/application narrative
