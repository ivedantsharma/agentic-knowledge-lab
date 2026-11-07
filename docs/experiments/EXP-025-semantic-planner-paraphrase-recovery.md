# EXP-025: Semantic Planner Recovers Paraphrases

## Goal

Test whether embedding-based semantic intent matching can recover planner performance on paraphrased questions that broke the exact-pattern rule planner.

## Previous result

Rule-based planner on paraphrases:

```text
InitialPlanRate = 0.0000
StoppedRate     = 0.0000
AnswerAccuracy  = 0.0000
```

## Semantic planner result

```text
tasks = 4
StoppedRate    = 1.0000
AnswerAccuracy = 1.0000
```

Goal classification was correct for all four tasks:

```text
mhp-001 → backup
mhp-002 → retry
mhp-003 → cache
mhp-004 → signing
```

Anchor detection was also correct:

```text
Atlas
Developer Productivity
Helios
Security Platform
```

## Interpretation

Embedding-based semantic intent matching removed the planner's dependence on exact surface phrasing.

The downstream retrieval, observation parsing, structured state, and stopping logic remained unchanged.

Therefore the performance recovery is attributable to the planner's improved language invariance.

## Important limitation

The semantic planner remains closed-world.

It can only choose among a fixed intent set:

- backup,
- retry,
- cache,
- signing.

It also generates queries from predefined templates.

So this is not yet open-ended planning.

## Next question

What happens when the user asks for a relation that is not represented by one of the planner's predefined intents?

That is the next failure mode to expose before introducing a generative planner.
