# Phase 0 Exercise Review — Foundations

This note records the first conceptual checkpoint and the corrections that matter for later phases.

## 1. LLM vs database

### Original understanding
An LLM does not store exact rows and columns like a traditional database. Instead it learns from data and uses learned representations/parameters to generate answers.

### Correction

This is broadly correct, with one important refinement:

An LLM does **not** normally take a query, generate a query embedding, and then search its own parameters for the nearest match.

A vector database behaves like:

```text
query
↓
query embedding
↓
nearest-neighbor search
↓
stored document embeddings
```

An LLM behaves more like:

```text
input tokens
↓
token embeddings
↓
transformer layers
↓
internal activations
↓
probabilities for the next token
```

Its parameters store distributed statistical patterns learned during training.

There is no explicit "row" saying:

```text
France | capital | Paris
```

and there is no normal nearest-neighbor lookup across the model weights during generation.

This distinction will become very important when we compare:
- parametric memory,
- retrieved external memory,
- vector databases.

---

## 2. Lexical vs dense vs hybrid retrieval

### Query 1
`RFC 7231 section 4.3`

**Best starting choice: Lexical**

Why:
- exact identifier,
- exact standard number,
- exact section number.

Semantic similarity is less important than matching the identifier precisely.

### Query 2
`How can I stop Python packages from conflicting between projects?`

**Best starting choice: Dense, or Hybrid**

Why:
A useful document may be titled:

```text
Using Python virtual environments
```

even though it does not use the exact phrase "stop packages from conflicting."

Dense retrieval can bridge that semantic gap.

Hybrid is also reasonable in a real production system.

### Query 3
`ERR_CONNECTION_REFUSED`

**Best starting choice: Lexical**

This is an important correction.

An error code/string is usually something we want to match almost exactly.

Lexical retrieval is excellent for:
- error messages,
- exception names,
- IDs,
- function names,
- product codes.

Dense retrieval can still help with explanations, but the exact error string is a very strong lexical signal.

### Query 4
`Ways to teach a model using rewards`

**Best starting choice: Dense**

Why:
Relevant documents may use terminology like:

```text
reinforcement learning
reward modeling
policy optimization
RLHF
```

without matching the original words exactly.

---

## 3. Why an agent may need multiple searches

Correct intuition:

The question contains dependent subproblems.

Example:

```text
Which company acquired Startup X,
and who was the CEO of that company
at the time of the acquisition?
```

Possible reasoning trajectory:

```text
Search Startup X acquisition
↓
discover Company Y
↓
discover acquisition date
↓
search Company Y CEO around that date
↓
verify temporal evidence
↓
answer
```

Important refinement:

A single retrieval call is not inherently incapable of retrieving multiple sources.

A retriever can return many documents in one search.

The deeper reason agentic search helps is that **later searches can depend on facts discovered in earlier searches**.

Before finding Company Y, we may not even know what the second search query should be.

This is called a dependent or multi-hop information need.

---

## 4. Why 100 documents may be worse than 5 relevant documents

Correct points:
- more tokens,
- more latency,
- more compute/cost,
- more irrelevant information,
- greater chance the model focuses on distractors.

Refinement:

We should avoid saying that more documents automatically "cause hallucination."

A better statement is:

> More irrelevant or conflicting context can increase distraction and reduce grounded answer quality.

The goal of retrieval is not:

```text
retrieve as much as possible
```

It is:

```text
retrieve enough high-quality evidence to answer correctly
while minimizing irrelevant context
```

This is one of the core optimization problems in our project.

---

# Key mental models after this checkpoint

## Parametric memory

Knowledge implicitly represented inside model parameters.

## External memory

Knowledge stored outside the model:
- documents,
- databases,
- vector indexes,
- graphs.

## Retrieval

Selecting useful external information for the current question.

## Agentic retrieval

The system can make multiple retrieval decisions where later actions depend on earlier observations.
