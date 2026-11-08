# EXP-062: Semantic Relation-Path Selection

## Research question

Given a gold start entity and several valid outgoing graph paths, can semantic path ranking select the relation path that matches the natural-language question?

## Why a branching graph is necessary

The original Phase 6 graph has very little branching.

A relation selector could appear perfect simply because there is only one possible route.

EXP-062 adds distractor branches using facts already present in the Phase 3 corpus.

Examples:

```text
Atlas
├── operated_by → Platform Reliability → ...
└── deployment_snapshot_cadence → once per day

Platform Reliability
├── maintains_storage_system → Borealis
└── maintains_legacy_storage_system → Aurora
```

## Controlled assumptions

Still oracle:

- start entity.

No longer oracle:

- relation path.

## Method

1. Enumerate simple paths from the start entity.
2. Stop candidate paths when they reach a literal value.
3. Render each path using relation names and supporting evidence.
4. Embed the user question and each candidate path profile with MiniLM.
5. Rank by cosine similarity.

## Metrics

- PathSelectionAccuracy
- AnswerAccuracy
- AvgCandidatePaths

## What success would mean

The system can choose among explicit structured routes from natural-language intent.

## What it would not mean

It would not yet prove:

- automatic start-entity linking,
- robust path selection on large graphs,
- learned graph planning,
- production-scale graph search.
