# Phase 1 — Research Plan v0.1

## 1. Research program

We are building two connected systems:

### Project A — Agent-Native Knowledge Engine

A knowledge retrieval system that progresses from simple retrieval baselines to adaptive, agentic retrieval over richer information architectures.

### Project B — KnowledgeBench

An evaluation framework that measures whether knowledge-search agents retrieve the right evidence, answer correctly, use tools efficiently, and handle difficult failure modes.

The projects form one research loop:

```text
Hypothesis
↓
Build system
↓
Evaluate on KnowledgeBench
↓
Inspect failures
↓
Modify architecture / retrieval policy
↓
Re-run
```

---

## 2. Primary research questions

### RQ1 — Information architecture

Can information architectures designed for LLM agents improve multi-hop retrieval accuracy and/or reduce context-token usage compared with flat fixed-size chunk retrieval?

### RQ2 — Retrieval policy

Can an adaptive retrieval policy choose among lexical, dense, hierarchical, and graph retrieval more effectively than a static retrieval strategy?

### RQ3 — Training

Does supervised fine-tuning or reinforcement-based training improve retrieval-tool selection compared with prompt-only behavior?

### RQ4 — Failure modes

Which failure modes dominate agentic knowledge retrieval under multi-hop, ambiguous, contradictory, temporal, adversarial, and unanswerable tasks?

---

## 3. Working hypotheses

### H1
Hierarchical or structured information representations will outperform flat fixed-size chunks on at least some multi-hop tasks.

### H2
Hybrid retrieval will outperform lexical-only and dense-only retrieval on a mixed benchmark containing both exact-match and semantic queries.

### H3
An adaptive policy can reduce unnecessary retrieval/tool calls while maintaining or improving answer accuracy.

### H4
Prompt-only agents will exhibit systematic tool-selection failures that can potentially be reduced by SFT and/or RL.

### H5
Improvements in final-answer accuracy may hide retrieval failures, so evaluation must separately measure evidence quality, retrieval quality, and final answers.

These are hypotheses, not goals to prove.

Negative results are valid.

---

## 4. Baselines

We must compare every complex system against simpler systems.

### Retrieval baselines

B0 — No retrieval / model-only answer, where appropriate.

B1 — Lexical retrieval (BM25).

B2 — Dense retrieval.

B3 — Hybrid lexical+dense retrieval.

B4 — Hybrid + reranker.

### Agent baselines

A0 — Single retrieval call.

A1 — Prompt-only agent with multiple retrieval tools.

A2 — Prompt-only agent + richer information architecture.

A3 — SFT retrieval-policy agent.

A4 — RL-trained retrieval-policy agent.

We should not claim an advanced system helps unless it beats a relevant simpler baseline.

---

## 5. Evaluation levels

We will measure the system at several levels.

### Level 1 — Retrieval

Did the retriever find the required evidence?

Example metrics:
- Recall@K
- Precision@K
- MRR
- nDCG where relevant

### Level 2 — Evidence

Did the selected evidence actually support the answer?

Example metrics:
- evidence recall
- evidence precision
- citation correctness
- source quality

### Level 3 — Answer

Did the system produce the correct final answer?

Example metrics:
- exact match for short factual answers
- normalized exact match
- F1 where appropriate
- rubric/model grader for open-ended synthesis

### Level 4 — Agent behavior

Did the agent solve the task efficiently?

Example metrics:
- number of tool calls
- number of retrieval rounds
- context tokens
- latency
- cost
- search depth
- repeated/duplicate searches
- stopping behavior

### Level 5 — Robustness

Can the system handle difficult cases?

Example categories:
- distractors
- contradictory evidence
- stale/temporal evidence
- entity ambiguity
- unanswerable questions
- prompt injection in retrieved documents
- long-context distraction
- search loops

---

## 6. Experimental principles

### P1 — Change one meaningful variable at a time

If we change chunking, retriever, prompt, embedding model, and reranker simultaneously, we cannot know what caused the result.

### P2 — Keep datasets fixed during direct comparisons

Do not compare two systems on different task sets and call the score difference an architectural improvement.

### P3 — Record configurations

Every experiment should record:
- model
- embedding model
- prompts
- retrieval K
- random seed when applicable
- dataset version
- architecture version
- relevant package versions

### P4 — Run repeated trials for stochastic agents

Agent trajectories can vary across runs.

Single-run success is not enough.

### P5 — Read traces, not only aggregate scores

A score can hide:
- grader bugs
- lucky answers
- wrong evidence
- inefficient search
- pathological behavior.

### P6 — Separate development and evaluation sets

Do not repeatedly tune on the final evaluation set.

### P7 — Prefer simple systems first

Complexity must earn its place through measured improvements.

---

## 7. Dataset strategy

We will eventually use a combination of:

### Controlled synthetic corpus

Useful because:
- we know the exact ground truth,
- we can generate adversarial cases,
- we can isolate failure modes.

### Public document corpus

Useful because:
- language and structure are realistic,
- retrieval is less artificial.

### Hand-authored hard tasks

Useful for:
- multi-hop
- ambiguity
- temporal conflicts
- contradiction
- adversarial retrieval

### Existing benchmark inspiration

We will study public agent-search benchmarks and eval methodology, but KnowledgeBench should test our own research questions rather than simply clone another benchmark.

---

## 8. First benchmark taxonomy

KnowledgeBench v1 should eventually include:

K1 — Direct retrieval  
K2 — Semantic paraphrase  
K3 — Exact identifier / lexical lookup  
K4 — Multi-hop composition  
K5 — Distractor-heavy retrieval  
K6 — Entity ambiguity  
K7 — Contradictory evidence  
K8 — Temporal/stale evidence  
K9 — Unanswerable questions  
K10 — Search-loop traps  
K11 — Retrieved prompt injection  
K12 — Long-context distraction

Not every category must exist in the first implementation.

---

## 9. What Phase 1 will deliver

Before starting the BM25 implementation, Phase 1 should produce:

1. research plan
2. evaluation metric definitions
3. dataset design
4. KnowledgeBench v0 task schema
5. high-level system architecture
6. experiment protocol
7. literature notes
8. first ADRs for major baseline choices

---

## 10. Phase 1 exit criterion

Phase 1 is complete when we can answer:

> If System X scores better than System Y, exactly what changed, what dataset was used, what metric improved, and why should we believe the comparison is fair?

If we cannot answer that, we are not ready to run meaningful research experiments.
