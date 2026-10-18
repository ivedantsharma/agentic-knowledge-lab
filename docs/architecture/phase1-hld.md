# Phase 1 High-Level Design

## 1. Goal

Build the foundation for an agent-native knowledge system and a rigorous benchmark capable of measuring retrieval, evidence, answer, and agent behavior.

Phase 1 focuses on research scaffolding rather than production-scale retrieval.

## 2. Major subsystems

### Knowledge Engine

Responsibilities:
- store/retrieve documents
- expose lexical retrieval
- expose dense retrieval
- expose hybrid retrieval baselines

Current components:

```text
knowledge_engine/
  retrieval/
    bm25.py
    hybrid.py
```

Dense retrieval currently lives in experiment runners and will later be promoted behind a common retriever interface.

### KnowledgeBench

Responsibilities:
- define benchmark tasks
- define corpus documents
- load versioned JSONL datasets
- represent system outputs
- compute retrieval metrics
- aggregate by category
- compare systems fairly

Current structure:

```text
knowledgebench/
  tasks/
    schema.py
    loader.py

  documents/
    schema.py
    loader.py

  runs/
    schema.py

  metrics/
    retrieval.py

  evaluation/
    retrieval_evaluator.py
    benchmark_evaluator.py
    category_evaluator.py
```

## 3. Core data model

### KnowledgeTask

Ground truth.

Contains:
- task_id
- question
- relevant_document_ids
- category
- expected_answer
- metadata

### KnowledgeDocument

Corpus item.

Contains:
- document_id
- text
- metadata

### RunResult

Observed system output.

Contains:
- task_id
- generated_answer
- retrieved_document_ids
- tool_calls
- latency_ms
- metadata

Important invariant:

```text
KnowledgeTask = what should be true
RunResult     = what the system actually did
```

Ground truth must not leak into system output objects.

## 4. Data flow

```text
tasks.jsonl
      \
       \
        -> validated schemas
       /
docs.jsonl
    |
    v
retriever / agent
    |
    v
RunResult[]
    |
    v
evaluator
    |
    +--> Recall@K
    +--> Precision@K
    +--> MRR
    +--> category slices
    +--> unanswerable diagnostics
```

## 5. Retrieval baselines

### BM25

Lexical baseline.

Strength:
- exact terms
- opaque identifiers

Observed failure mode:
- semantic paraphrase can rank relevant evidence lower.

### Dense retrieval

Current model:
`all-MiniLM-L6-v2`

Strength:
- semantic paraphrase

Observed failure mode:
- near-identical opaque identifiers can be confused.

### Hybrid RRF

Current purpose:
- low-assumption rank-fusion baseline

Observed limitation:
- symmetric rank disagreements can produce ties.

No learned or tuned fusion is justified yet.

## 6. Evaluation philosophy

Separate:
- retrieval quality
- evidence quality
- answer quality
- agent behavior
- efficiency
- robustness

Phase 1 implements retrieval evaluation first.

Later phases extend the same architecture.

## 7. Phase 1 non-goals

Not yet included:
- production indexing
- chunking pipelines
- rerankers
- graph retrieval
- hierarchical retrieval
- multi-hop agents
- answer generation
- SFT
- RL
- distributed serving

Those belong to later phases.

## 8. Architectural principle

Prefer small explicit baselines before sophisticated systems.

Every added component should answer a measured failure rather than merely increasing system complexity.
