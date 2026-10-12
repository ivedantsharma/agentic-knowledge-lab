# Phase 0 — Real Embeddings, Stage B

Now we move from made-up vectors to vectors produced by a real embedding model.

## 1. What changes now?

In Stage A we manually wrote vectors like:

```text
A = [1, 0]
B = [0.9, 0.1]
```

Now the computer will generate the vectors from real text:

```text
"A dog is sleeping on the couch."
↓
embedding model
↓
[hundreds of numbers]
```

We will then compare those vectors using the cosine-similarity function we implemented ourselves.

## 2. Model choice

We will start with:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Why this model?

- small enough for a Codespace exercise,
- fast,
- widely used for semantic similarity,
- produces compact sentence embeddings,
- simple API,
- good teaching model before larger embedding systems.

This is not a claim that it is the best production model for our final project.

It is a teaching baseline.

## 3. The experiment

We will compare these sentences:

```text
S1 = "A dog is sleeping on the couch."
S2 = "A puppy is taking a nap on the sofa."
S3 = "The stock market increased today."
S4 = "Investors saw equity prices rise during trading."
```

Expected intuition:

- S1 and S2 should be relatively similar.
- S3 and S4 should be relatively similar.
- S1 and S3 should be much less similar.

## 4. Important idea: semantic similarity

Lexical overlap asks:

> Do these sentences share words?

Semantic similarity asks:

> Do these sentences mean similar things?

Example:

```text
"A dog is sleeping."
"A puppy is taking a nap."
```

The exact words differ, but the meanings are close.

That is the main reason dense retrieval exists.

## 5. What the model returns

The embedding model will return a vector for each sentence.

For this model, each sentence is represented by a fixed-length vector.

The individual numbers are not meant to be interpreted one by one.

What matters is the geometry of the whole vector.

## 6. Exercise goal

You will:

1. load the embedding model,
2. embed four sentences,
3. print the vector dimension,
4. compare sentence pairs using your cosine-similarity function,
5. inspect whether the scores match intuition.

## 7. Important engineering lesson

We are separating responsibilities:

```text
Embedding model
→ creates vectors

Your cosine function
→ compares vectors
```

Keeping components separate makes systems easier to understand, test, replace, and benchmark.

## 8. Later connection to retrieval

Soon we will do:

```text
documents
↓
embeddings
↓
store vectors

user query
↓
query embedding
↓
compare against document vectors
↓
rank documents
```

That is the core of dense retrieval.
