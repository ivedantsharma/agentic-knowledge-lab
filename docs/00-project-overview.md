# Project Overview

## Working title

**Agentic Knowledge Lab**

## Big idea

Traditional knowledge systems are often designed for humans: documents, folders, pages, chapters, and search boxes.

This project asks a different question:

> What happens if information is organized specifically for AI agents?

We will build a knowledge engine and an evaluation benchmark together.

## Project A — Agent-Native Knowledge Engine

Goal: build and compare multiple ways for an LLM agent to retrieve external knowledge.

Planned progression:
1. Keyword retrieval (BM25)
2. Dense/vector retrieval
3. Hybrid retrieval
4. Reranking
5. Agentic multi-step search
6. Hierarchical knowledge representation
7. Graph-based representation
8. Claim/evidence representation
9. Adaptive retrieval policy
10. SFT/RL experiments for tool selection

## Project B — KnowledgeBench

Goal: build difficult tasks that reveal where knowledge-search agents fail.

Planned categories:
- Direct retrieval
- Multi-hop reasoning
- Distractors
- Temporal conflicts
- Contradictory sources
- Entity ambiguity
- Needle-in-a-haystack
- Unanswerable tasks
- Search-loop traps
- Prompt-injection documents

## Research loop

Hypothesis → Build → Evaluate → Analyze failures → Improve → Repeat

## Success criteria

This project is not complete merely because a demo works.

We want:
- reproducible code
- tests
- HLD and LLD documentation
- Architecture Decision Records
- experiment records
- baselines
- metrics
- ablations
- failure analysis
- final research report
- resume claims backed by actual results
