# Glossary

This file is intentionally simple. We will expand each term as we learn it.

## LLM
**Large Language Model**

Simple explanation: a program trained on huge amounts of text that learns language patterns and can generate useful text.

## Token
A small piece of text that a language model reads. A token is not always a complete word.

## Context window
The amount of text/tokens a model can consider at one time.

Think of it as the size of the model's desk.

## Embedding
A list of numbers representing the meaning of some text.

Texts with similar meanings are usually represented by nearby points in embedding space.

## Retrieval
Finding relevant information from a larger collection.

## RAG
**Retrieval-Augmented Generation**

Typical flow:

Question → Search for relevant text → Give text to LLM → Generate answer

## Agent
A system where a model can repeatedly:
1. inspect its state,
2. choose an action,
3. use a tool,
4. observe the result,
5. continue until the task is solved or stopped.

## Tool
A capability the model can call, such as search, a database query, a calculator, or graph traversal.

## BM25
A classical text-search scoring algorithm.

Simple intuition: documents get rewarded when they contain important query words, while very common words matter less.

## Vector search
Searching by semantic similarity using embeddings.

## Hybrid retrieval
Combining keyword search and vector search.

## Reranker
A model or algorithm that reorders initially retrieved results based on estimated relevance.

## Fine-tuning
Continuing training of an existing model on a more specific dataset.

## SFT
**Supervised Fine-Tuning** — teaching a model using examples of desired input → output behavior.

## RL
**Reinforcement Learning** — teaching behavior using rewards or penalties.

## Benchmark
A fixed collection of tasks used to compare systems.

## Evaluation / Eval
A procedure that measures how well a model or system performs.

## Groundedness
Whether an answer is actually supported by provided or retrieved evidence.

## Ablation
Remove or alter one component and observe how performance changes.

## HLD
**High-Level Design** — the city map of the system: major components and how they communicate.

## LLD
**Low-Level Design** — the building blueprint: classes, interfaces, schemas, algorithms, data structures, errors, and implementation details.

## ADR
**Architecture Decision Record** — a short document recording a design choice, alternatives, rationale, and trade-offs.
