# Phase 0 Learning Module — LLMs, Tokens, Embeddings, RAG, and Agents

This document is our first conceptual lesson.

The goal is not to memorize definitions. The goal is to build a mental model of how the pieces fit together.

---

## 1. Large Language Model (LLM)

### Kid explanation

Imagine a machine that has read a gigantic library.

You give it some words, and it tries to guess what words should come next.

Example:

```text
The capital of France is ...
```

It predicts:

```text
Paris
```

### Engineer explanation

An LLM receives tokens, converts them into internal numerical representations, processes them through many transformer layers, and predicts probability distributions over possible next tokens.

Very simplified:

```text
Text
↓
Tokens
↓
Numerical vectors
↓
Transformer layers
↓
Next-token probabilities
↓
Generated text
```

### Important idea

An LLM is not a database.

It can contain a lot of learned information in its parameters, but that information is not stored as exact rows that we can reliably query.

That is one reason external retrieval systems matter.

---

## 2. Token

### Kid explanation

An LLM does not read whole paragraphs the way humans do.

It breaks text into smaller pieces called tokens.

Example:

```text
"unbelievable"
```

might become multiple token pieces rather than one full word.

### Why tokens matter

Models have context limits measured in tokens.

API costs are often related to token counts.

Retrieval systems also care about how many tokens of evidence are inserted into the prompt.

---

## 3. Context window

### Kid explanation

Imagine the model has a desk.

It can only keep a limited amount of paper on the desk at once.

That desk is the context window.

### Engineer explanation

The context window is the maximum number of tokens the model can process in one inference context.

The context typically includes:
- system instructions,
- conversation,
- retrieved documents,
- tool results,
- the user query,
- generated output.

### Why our project cares

If retrieval dumps too much irrelevant text into context:
- latency can increase,
- cost can increase,
- useful evidence can be harder to find,
- model performance may decrease.

So retrieval quality is not just about finding information.

It is also about choosing the **right amount of information**.

---

## 4. Embedding

### Kid explanation

Imagine every sentence becomes a point on a giant map of meaning.

Two sentences with similar meanings live close together.

Example:

```text
"The dog is sleeping."
"A puppy is taking a nap."
```

These may be far apart in exact words, but close in meaning.

### Engineer explanation

An embedding model maps text into a dense numerical vector.

Example:

```text
"The dog is sleeping."
↓
[0.12, -0.44, 0.81, ...]
```

Another semantically similar sentence may produce a nearby vector.

### Why this matters

We can turn both:
- user queries,
- document chunks

into vectors.

Then we can search for nearby vectors.

That is called dense or vector retrieval.

---

## 5. Lexical retrieval

### Kid explanation

This is search by matching words.

If you search:

```text
Python virtual environment
```

a lexical search system looks for documents containing important matching terms.

### Example algorithm

BM25.

We will study BM25 properly in Phase 3.

### Strengths

Lexical search is often good for:
- names,
- IDs,
- exact phrases,
- error messages,
- product codes,
- technical identifiers.

---

## 6. Dense retrieval

### Kid explanation

This is search by meaning.

You search:

```text
How do I isolate Python project dependencies?
```

and it may retrieve a document titled:

```text
Using virtual environments
```

even if the exact words do not match.

### Why it works

Both query and document are embedded into vector space.

Similarity is measured mathematically.

One common metric is cosine similarity.

---

## 7. RAG

RAG means **Retrieval-Augmented Generation**.

### Kid explanation

Instead of asking the model to answer only from memory, we let it look things up first.

### Basic flow

```text
Question
↓
Search
↓
Relevant documents
↓
LLM
↓
Answer
```

### Example

User asks:

```text
What did Company X report in its 2025 annual report?
```

A plain LLM may not know.

A RAG system can:

```text
Find the annual report
↓
retrieve the relevant section
↓
give it to the model
↓
generate an answer grounded in that evidence
```

### Important limitation

Basic RAG usually searches once.

Hard questions often require multiple searches.

That leads us to agents.

---

## 8. Agent

### Kid explanation

A normal RAG system asks a librarian one question.

An agent can keep asking follow-up questions until it has enough information.

### Example

Question:

```text
Which company acquired X, and what product did it launch two years later?
```

The agent may do:

```text
Search acquisition of X
↓
Find company Y
↓
Search company Y product launches
↓
Find product Z
↓
Verify date
↓
Answer
```

### Engineer explanation

An agent usually has:

- state,
- model,
- tools,
- observations,
- stopping rules.

Conceptually:

```python
while not finished:
    action = model.choose_action(state)
    observation = execute(action)
    state = update(state, observation)
```

---

## 9. Tool

A tool is an external capability the model can invoke.

Examples:

- keyword search
- vector search
- SQL query
- calculator
- graph traversal
- API call

The model decides which tool to use and with what arguments.

---

## 10. The full mental model

Our final system will eventually look approximately like this:

```text
User Question
    ↓
Query Understanding
    ↓
Agent / Planner
    ↓
Choose Tool
    ↓
┌───────────────┬───────────────┬───────────────┐
│               │               │
BM25         Vector Search    Graph Search
│               │               │
└───────────────┴───────────────┴───────────────┘
                ↓
           Evidence
                ↓
           Verification
                ↓
             Answer
```

KnowledgeBench will evaluate whether this system:
- found the right evidence,
- answered correctly,
- used good sources,
- avoided unnecessary searches,
- stopped at the right time,
- handled conflicting information,
- recognized unanswerable questions.

---

# Tiny hands-on exercises

These are intentionally simple.

## Exercise 1 — LLM vs database

Answer in your own words:

Why is an LLM not the same thing as a database?

## Exercise 2 — Lexical vs dense retrieval

For each query, guess which method may be stronger:

1. `RFC 7231 section 4.3`
2. `How can I stop Python packages from conflicting between projects?`
3. `ERR_CONNECTION_REFUSED`
4. `Ways to teach a model using rewards`

Choose:
- lexical,
- dense,
- or hybrid.

Explain why.

## Exercise 3 — RAG vs agent

Suppose the question is:

```text
Which company acquired Startup X, and who was the CEO of that company at the time of the acquisition?
```

Explain why one search may not be enough.

## Exercise 4 — Context budget

Why might retrieving 100 documents be worse than retrieving 5 very relevant documents?

---

# Phase 0 learning checkpoint

Before moving to Phase 1, you should be able to explain:

- What is an LLM?
- What is a token?
- What is a context window?
- What is an embedding?
- What is lexical retrieval?
- What is dense retrieval?
- What is RAG?
- What is an agent?
- What is a tool?
- Why do agents need evaluation?

You do not need mathematical depth yet.
