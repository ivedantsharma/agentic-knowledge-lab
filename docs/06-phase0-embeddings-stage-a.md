# Phase 0 — Embeddings and Cosine Similarity, Stage A

Before using a real embedding model, we will understand the math with tiny made-up vectors.

---

## 1. What is a vector?

A vector is simply an ordered list of numbers.

Example:

```text
A = [1, 2]
```

You can imagine this as a point on a 2D map:

- move 1 unit on the x-axis,
- move 2 units on the y-axis.

Real embedding vectors usually have hundreds or thousands of dimensions, but the idea is the same.

---

## 2. Why embeddings are vectors

An embedding model converts text into numbers.

Example:

```text
"A dog is sleeping."
↓
[0.12, -0.44, 0.81, ...]
```

Those numbers are not individually human-readable.

What matters is that semantically similar text tends to produce vectors that point in similar directions.

---

## 3. Comparing two vectors

Suppose:

```text
A = [1, 0]
B = [0.9, 0.1]
C = [0, 1]
```

Intuitively:

- A and B point almost the same way.
- A and C point in very different directions.

We want a mathematical way to measure this.

One common method is **cosine similarity**.

---

## 4. Dot product

For:

```text
A = [a1, a2]
B = [b1, b2]
```

the dot product is:

```text
A · B = a1*b1 + a2*b2
```

Example:

```text
A = [1, 2]
B = [3, 4]

A · B
= 1*3 + 2*4
= 3 + 8
= 11
```

---

## 5. Vector magnitude

Magnitude means the length of a vector.

For:

```text
A = [a1, a2]
```

the magnitude is:

```text
||A|| = sqrt(a1^2 + a2^2)
```

Example:

```text
A = [3, 4]

||A||
= sqrt(3^2 + 4^2)
= sqrt(9 + 16)
= sqrt(25)
= 5
```

---

## 6. Cosine similarity

Formula:

```text
cosine_similarity(A, B)
=
(A · B) / (||A|| * ||B||)
```

This compares the **direction** of two vectors.

Typical interpretation:

```text
 1.0  -> same direction
 0.0  -> perpendicular / unrelated direction
-1.0  -> opposite direction
```

For many modern text embeddings, higher cosine similarity usually means more semantic similarity.

---

## 7. Why cosine similarity instead of raw distance?

Suppose:

```text
A = [1, 1]
B = [10, 10]
```

Their magnitudes are very different.

But they point in exactly the same direction.

Cosine similarity focuses on direction rather than absolute size.

That is often useful for semantic embeddings.

---

## 8. Manual example

Take:

```text
A = [1, 0]
B = [0.9, 0.1]
C = [0, 1]
```

### A vs B

Dot product:

```text
1*0.9 + 0*0.1 = 0.9
```

Magnitude of A:

```text
sqrt(1^2 + 0^2) = 1
```

Magnitude of B:

```text
sqrt(0.9^2 + 0.1^2)
= sqrt(0.82)
≈ 0.9055
```

Cosine similarity:

```text
0.9 / (1 * 0.9055)
≈ 0.994
```

Very similar.

### A vs C

Dot product:

```text
1*0 + 0*1 = 0
```

Cosine similarity:

```text
0
```

Very different direction.

---

## 9. Important warning

Cosine similarity does not magically understand language.

The **embedding model** is what learns how to map language into vectors.

Cosine similarity only compares the vectors produced by that model.

So the system is:

```text
text
↓
embedding model
↓
vector
↓
cosine similarity
↓
similarity score
```

---

# Exercise

Implement these functions yourself in:

`scripts/cosine_similarity_exercise.py`

You should implement:

1. `dot_product(a, b)`
2. `magnitude(v)`
3. `cosine_similarity(a, b)`

Do not use NumPy for this exercise.

After implementing, run:

```bash
uv run python scripts/cosine_similarity_exercise.py
```

Expected approximate output:

```text
A vs B: 0.9939...
A vs C: 0.0
```

Then run:

```bash
uv run pytest
```

We will review your implementation before moving to real embeddings.
