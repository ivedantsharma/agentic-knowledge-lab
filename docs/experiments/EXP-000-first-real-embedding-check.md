# EXP-000: First Real Embedding Similarity Check

## Goal

Verify that a real sentence-embedding model maps semantically related sentences to vectors with higher cosine similarity than unrelated sentences.

## Model

`sentence-transformers/all-MiniLM-L6-v2`

## Environment

- Python: 3.12.15
- Embedding dimension: 384
- Runtime: GitHub Codespaces

## Sentences

- S1: "A dog is sleeping on the couch."
- S2: "A puppy is taking a nap on the sofa."
- S3: "The stock market increased today."
- S4: "Investors saw equity prices rise during trading."

## Results

| Pair | Cosine similarity |
|---|---:|
| S1 vs S2 | 0.7644 |
| S1 vs S3 | -0.0648 |
| S3 vs S4 | 0.6223 |

## Interpretation

The results match our semantic intuition:

- S1 and S2 describe nearly the same scene despite using different words.
- S3 and S4 are both about financial markets rising.
- S1 and S3 are unrelated and received a very low/slightly negative similarity score.

This demonstrates the basic mechanism behind dense retrieval:

```text
text
↓
embedding model
↓
vector
↓
cosine similarity
↓
semantic ranking
```

## Important limitation

This experiment does not prove that the model is universally good at semantic retrieval.

It only demonstrates expected behavior on a tiny illustrative example.

Later experiments will use larger datasets and retrieval metrics such as Recall@K and MRR.
