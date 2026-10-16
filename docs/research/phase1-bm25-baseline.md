# Phase 1 — BM25 Lexical Retrieval Baseline

We already have a dense retrieval baseline.

Now we need a lexical baseline.

## 1. What problem does BM25 solve?

Suppose the query is:

```text
ERR_CONNECTION_REFUSED
```

A lexical system can strongly reward a document containing that exact technical token.

BM25 ranks documents using word overlap, but it does more than simply count matching words.

It accounts for:

- term frequency,
- document frequency,
- document length.

---

## 2. Kid explanation

Imagine searching five books.

If your query contains:

```text
python dependency conflict
```

a book gets points when it contains those words.

But:

- a rare word should count more than a common word,
- repeating a word 100 times should not give unlimited points,
- a huge document should not win simply because it contains more words.

BM25 handles those effects.

---

## 3. Engineer explanation

For each query term, BM25 combines:

### Term frequency

How often does the term occur in this document?

More occurrences can help, but with diminishing returns.

### Inverse document frequency

How rare is this term across the corpus?

A term occurring in almost every document is not very discriminative.

A rare technical identifier can be extremely useful.

### Length normalization

Long documents naturally contain more words.

BM25 normalizes for document length so long documents do not receive an unfair advantage.

---

## 4. Simplified scoring formula

For query term q and document D:

```text
score(q, D)
=
IDF(q)
*
TF_component(q, D)
```

A common BM25 form is:

```text
IDF(q)
=
log(
    1 +
    (N - df(q) + 0.5)
    /
    (df(q) + 0.5)
)
```

where:

- N = total number of documents
- df(q) = number of documents containing q

The term-frequency part is:

```text
tf * (k1 + 1)
-----------------------------
tf + k1 * (1 - b + b * dl/avgdl)
```

where:

- tf = term frequency in the document
- dl = document length
- avgdl = average document length
- k1 controls term-frequency saturation
- b controls document-length normalization

We will start with:

```text
k1 = 1.5
b = 0.75
```

These are baseline choices, not sacred constants.

---

## 5. Tokenization

BM25 operates on tokens.

For this first baseline we use a deliberately simple tokenizer:

- lowercase text,
- keep letters/numbers/underscores,
- split everything else.

This preserves technical identifiers such as:

```text
err_connection_refused
```

while remaining easy to understand.

Later tokenization itself can become an experimental variable.

---

## 6. Dense vs BM25

Dense retrieval:

```text
query
↓
embedding
↓
semantic similarity
```

BM25:

```text
query
↓
tokens
↓
lexical overlap + IDF + length normalization
```

Neither is universally better.

That is why we benchmark both.

---

## 7. Controlled experiment

We will compare:

```text
BM25
vs
all-MiniLM-L6-v2 dense retrieval
```

while keeping fixed:

- corpus
- benchmark tasks
- k = 3
- evaluator
- relevance judgments

The primary changed variable is retrieval method.

That makes the comparison interpretable.

---

## 8. Important expectation

Our current benchmark is tiny and easy.

It is possible that both systems score perfectly.

That would not mean:

```text
BM25 = dense retrieval universally
```

It would mean:

```text
this benchmark is not yet difficult enough to distinguish them
```

That itself is useful benchmark-design evidence.
