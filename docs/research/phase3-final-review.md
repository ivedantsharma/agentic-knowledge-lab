# Phase 3 Final Review

## Status

Phase 3 complete.

## Objective

Understand and implement deterministic multi-hop retrieval before introducing autonomous agent planning.

## What was built

### Benchmark infrastructure

- EvidenceHop
- MultiHopTask
- multi-hop task loader
- multi-document synthetic corpora
- two-hop and three-hop benchmark tasks

### Execution

- one-shot dense baseline
- deterministic gold-hop retrieval
- query templates
- intermediate fact chaining
- extracted-fact chaining
- structured retrieval state

### Evaluation

- Hop Accuracy
- Exact Chain Match
- Fact Accuracy
- Answer Accuracy

### Failure analysis

Phase 3 produced several useful findings.

#### Finding 1 — one-shot retrieval can fail on compositional questions

The original full question ranked an Atlas backup distractor first.

#### Finding 2 — decomposition repaired retrieval

Focused hop queries recovered the correct evidence chain.

#### Finding 3 — intermediate fact extraction can drive later searches

The system successfully used facts extracted from one document to formulate the next query.

#### Finding 4 — multi-hop errors can propagate

A wrong or under-specified intermediate state can change all later retrieval behavior.

#### Finding 5 — state compression can lose critical information

Reducing:

```text
Borealis + production
```

to:

```text
Borealis
```

caused staging evidence to outrank production evidence.

#### Finding 6 — structured state repaired the failure

Preserving the production qualifier restored the correct ranking.

#### Finding 7 — the mechanism generalized beyond one chain

Final benchmark:

```text
tasks = 4
hops = 10

HopAccuracy          = 1.0000
ExactChainMatchRate  = 1.0000
FactAccuracy         = 1.0000
AnswerAccuracy       = 1.0000
```

## What Phase 3 does NOT claim

The system does not yet autonomously:

- decompose questions,
- choose tools,
- generate search queries,
- choose hop count,
- decide when to stop,
- recover from uncertainty.

The benchmark is synthetic.

The extraction rules and query templates are benchmark-authored.

## Phase 4 handoff

Phase 4 is:

# Agentic Search Planner

The central question changes from:

> Can the system execute a known retrieval chain?

to:

> Can the system decide and execute the retrieval chain itself?

Phase 4 should introduce, gradually:

1. explicit planner state,
2. planner actions,
3. search-tool abstraction,
4. query generation,
5. stopping conditions,
6. trace recording,
7. planner evaluation.

The Phase 3 executor should remain available as an oracle / deterministic baseline for comparison.
