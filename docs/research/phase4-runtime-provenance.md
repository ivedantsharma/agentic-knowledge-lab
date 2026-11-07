# Phase 4 — Runtime Provenance for Agent Experiments

## Why this debugging step exists

The repository version of the Qwen continuation planner contains a grounded STOP gate.

The observed runtime behavior was inconsistent with that implementation.

This creates a new class of failure:

```text
experiment code != code we think we are running
```

Before interpreting model behavior, we must verify runtime provenance.

## New diagnostics

The experiment now prints:

```text
qwen_planner_module=<actual imported file path>
qwen_planner_version=grounded-stop-v2
```

At each continuation decision it also prints:

```text
answerable=<bool>
candidate_answer=<model output or None>
grounded=<bool>
```

## Why this matters

Reproducible research requires not only:

- dataset version,
- model version,
- prompt version,

but also:

- code version,
- imported module path,
- decision trace.

If stale code is running, model conclusions drawn from the output are invalid.

## Expected intermediate behavior

On the organization document:

```text
answerable=True   # Qwen may still be overconfident
candidate_answer='Failed jobs are sent to the developer\'s own platform.'
grounded=False
```

Because `grounded=False`, the planner must continue with SEARCH.

If the runtime instead reports a STOP immediately, the printed module path/version will tell us which implementation actually executed.
