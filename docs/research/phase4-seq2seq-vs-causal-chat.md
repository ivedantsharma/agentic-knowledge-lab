# Phase 4 — Seq2Seq Models vs Causal Chat Models for Planning

## FLAN-T5 so far

FLAN-T5 is an encoder-decoder sequence-to-sequence model.

Conceptually:

```text
input text
↓
encoder
↓
internal representation
↓
decoder
↓
output text
```

This architecture is well suited to transformations such as:

- translation,
- summarization,
- classification-as-text,
- answer extraction.

Our experiments show that FLAN-T5 can indeed perform grounded extraction.

## Planner difficulty

The planner needs a different behavior:

```text
question + partial state
↓
infer missing information
↓
invent next action/query
```

That is closer to conversational instruction following and open-ended generation.

## Causal language model

A causal language model predicts the continuation of a token sequence.

Conceptually:

```text
system message
user message
assistant:
↓
generate continuation
```

Modern instruction-tuned chat models are usually trained specifically to follow role-based conversations and produce assistant responses.

## Chat template

A chat model does not receive plain strings exactly as humans see them.

The tokenizer converts messages such as:

```text
system: You are a search planner.
user: Generate the next search query...
```

into the special token format expected during instruction tuning.

Hugging Face exposes this through:

```python
tokenizer.apply_chat_template(...)
```

Using the correct chat template matters because it makes inference match the format used during post-training.

## Next baseline

We use:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

The important experimental change is not simply that it has more parameters.

It is a different:

- architecture,
- tokenizer,
- post-training recipe,
- chat/instruction interface.

Therefore this is a **model-family ablation**, not a pure capacity ablation.

## Research question

With the exact same five capability probes, does a small chat-oriented instruction model perform open-ended query generation better than the FLAN-T5 family?
