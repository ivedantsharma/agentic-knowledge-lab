# EXP-040: Child Retrieval Query Refinement

## Motivation

EXP-039 achieved perfect parent routing but failed to distinguish Retry Policy from Dead Letter Handling inside the Cirrus manual.

## Research question

Does a more focused child-stage query improve within-document section ranking while keeping the parent stage unchanged?

## Controlled variables

Keep fixed:

- corpus
- questions
- document representations
- MiniLM model
- cosine similarity
- parent retrieval
- candidate set.

Change only:

- child-stage query.

## Baseline child query

```text
original user question
```

## Refined child query

For the first version, use a deterministic evidence-seeking rewrite that emphasizes the requested relation.

Examples:

```text
Where are Cirrus jobs sent after exhausting all retries?
→ destination after all retry attempts
```

```text
How often do Borealis incremental backups run?
→ incremental backup cadence
```

```text
What is the current Atlas signing-key identifier?
→ current signing-key identifier
```

## Why deterministic first?

The goal is to test whether child ranking is sensitive to query focus.

Using an LLM rewrite immediately would change both:

- query formulation strategy
- retrieval topology experiment.

We want one meaningful variable at a time.

## Metrics

- parent DocumentHit@1
- original child SectionHit@1
- refined child SectionHit@1
- per-task rank changes.

## Interpretation

If Cirrus improves while other tasks remain stable, the failure is partly a query-representation problem.

If it does not improve, the next step is a stronger child scorer such as a cross-encoder.