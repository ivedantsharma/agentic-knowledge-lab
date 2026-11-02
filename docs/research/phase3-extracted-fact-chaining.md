# Phase 3 — Extracted-Fact Chaining

## What changed?

The previous experiment used:

```text
previous_fact = hop.expected_fact
```

That means the benchmark supplied the intermediate answer.

This experiment removes that shortcut.

The new loop is:

```text
render query
↓
retrieve top-1 document
↓
extract fact from retrieved text
↓
use extracted fact in next query template
↓
repeat
```

## Why use regex first?

We are not claiming regex is a general knowledge extractor.

It is a controlled baseline.

A simple relation such as:

```text
Atlas is operated by the Platform Reliability team.
```

can be extracted with:

```text
operated by the (.+?) team
```

The capture group returns:

```text
Platform Reliability
```

The important experimental change is not the sophistication of the extractor.

It is that the next query now depends on information read from the retrieved document rather than a gold benchmark value.

## Dataset versioning

The earlier experiments used:

```text
phase3_multihop_tasks_v0.json
```

We preserve that file unchanged.

This experiment uses:

```text
phase3_multihop_tasks_v1.json
```

which adds extraction patterns.

This avoids silently changing the dataset used for already-reported experiments.

## New metric: Fact Accuracy

Retrieval correctness is not enough anymore.

We now evaluate:

- Hop Accuracy: did we retrieve the right document?
- Exact Chain Match: did we retrieve the whole ordered chain?
- Fact Accuracy: did we extract the correct fact at each hop?
- Answer Correct: did the final extracted fact equal the task answer?

These metrics separate retrieval failures from extraction failures.

## Limitation

The extraction rule is still benchmark-authored.

The system does not yet infer which span matters.

That will be the next abstraction after this baseline is validated.
