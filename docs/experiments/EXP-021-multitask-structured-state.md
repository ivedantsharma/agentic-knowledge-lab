# EXP-021: Multi-Task Structured-State Benchmark

## Goal

Evaluate the structured multi-hop retrieval executor across several independent tasks rather than one handcrafted chain.

## Benchmark

```text
tasks = 4
total hops = 10
```

Task families:

- Atlas → Platform Reliability → Borealis → backup cadence
- Developer Productivity → Cirrus → retry limit
- Helios → Identity Foundations → Solstice → cache duration
- Security Platform → Meridian → signing-key rotation

The benchmark includes:

- two-hop chains,
- three-hop chains,
- production versus staging/development distractors,
- relation-level distractors,
- structured state propagation.

## Aggregate results

```text
HopAccuracy          = 1.0000
ExactChainMatchRate  = 1.0000
FactAccuracy         = 1.0000
AnswerAccuracy       = 1.0000
```

## Interpretation

The structured-state executor successfully:

1. retrieved the correct document at each hop,
2. extracted the expected intermediate fact,
3. preserved qualifiers when required,
4. rendered the next query from state,
5. reached the correct final answer.

This is stronger evidence than the earlier single-task experiments.

## Important limitation

The benchmark remains synthetic and deterministic.

The system is still given:

- the hop sequence,
- query templates,
- extraction patterns,
- stopping point.

Therefore these results do not demonstrate autonomous agent planning.

They demonstrate that the underlying multi-hop execution machinery is working reliably on the current benchmark.

## Phase 3 conclusion

The main Phase 3 research question was:

> Can a deterministic multi-step retrieval process solve compositional questions that one-shot retrieval fails to solve reliably?

On this synthetic benchmark, yes.

The single-hop baseline failed on the original compositional question.

The structured multi-hop executor recovered the evidence chain and generalized across four task families.
