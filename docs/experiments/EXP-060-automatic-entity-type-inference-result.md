# EXP-060 Result: Automatic Lexical Entity-Type Inference

## Aggregate

```text
TypeInferenceAccuracy=0.6667
ResolvableEntityAccuracy=0.5000
AbstentionAccuracy=1.0000
FalsePositiveResolutionRate=0.0000
```

## Failure pattern

Two positive tasks failed before semantic ranking:

```text
"team operating the Atlas authentication service"
"group maintaining the production session metadata cache"
```

The baseline type inferer found both team and service cues in each phrase and treated that as ambiguous.

For example:

```text
team      -> team cue
service   -> service cue
```

and:

```text
group     -> team cue
cache     -> service cue
```

## Diagnosis

The policy treats every type word in the mention as if it described the referent.

That is incorrect for relational noun phrases.

The first noun-like type cue describes the target entity, while later type words may describe related objects.

## Conclusion

Do not change the semantic model or threshold.

EXP-061 will compare the original conflict-abstain policy with an earliest-cue policy while keeping all downstream components fixed.
