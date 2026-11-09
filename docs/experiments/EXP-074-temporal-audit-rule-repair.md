# EXP-074: Temporal Integrity Audit Rule Repair

## Research question

Can the integrity audit validate temporal tasks without falsely requiring every multi-hop bridge document to be temporally versioned?

## Problem exposed by EXP-073

The original rule treated all supporting documents as if they were temporal policy records.

That is too strict for compositional tasks.

Example:

```text
Atlas ownership              → undated relationship fact
Platform Reliability storage → dated/current relationship or policy
Borealis backup policy       → dated current fact
Borealis previous policy     → dated stale fact
```

Only the temporal current/stale evidence needs version metadata.

## Controlled change

Keep fixed:

- hard benchmark v0,
- all documents,
- all task annotations.

Change only the audit rule.

## Repaired rule

For every `stale_knowledge` task:

- at least one stale document must exist,
- every stale document must have `effective_at`,
- at least one supporting document must have `effective_at`,
- other supporting bridge documents may be undated.

## Why this is better

It tests the property we actually care about:

```text
Can current vs stale evidence be temporally distinguished?
```

without demanding artificial dates for unrelated graph/ownership facts.

## Success criterion

The unchanged hard-v0 benchmark should pass the repaired audit if no other integrity defect exists.
