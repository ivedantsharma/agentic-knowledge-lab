# Phase 1 Literature Notes — Retrieval, Context, and Evals

These notes connect our Phase 1 design choices to external guidance.

## Anthropic: Introducing Contextual Retrieval

Source:
https://www.anthropic.com/engineering/contextual-retrieval

Key points relevant to this project:

- Dense embeddings are useful for semantic relationships but can miss crucial exact matches.
- BM25 contributes exact lexical matching.
- Anthropic describes combining BM25 and embedding retrieval with rank fusion before reranking.
- Retrieval quality depends on chunk boundaries, embedding choice, top-k, and reranking.
- Contextualizing chunks before indexing can improve retrieval when standalone chunks lose document-level meaning.
- Anthropic reports substantial reductions in top-20 retrieval failure from contextual embeddings/BM25 and further gains from reranking.

Connection to our experiments:

Our v1/v2 synthetic experiments independently reproduced the qualitative complementarity:
- dense retrieval handled semantic paraphrase well,
- BM25 handled an opaque exact identifier better.

Our equal-weight RRF baseline did not improve v2 because one direct rank disagreement produced a symmetric fusion tie.

We should therefore keep hybrid retrieval as a baseline but postpone tuning/learned fusion until a larger dev set exists.

## Anthropic: Building Effective Agents

Source:
https://www.anthropic.com/engineering/building-effective-agents

Key point relevant to this project:

Anthropic emphasizes simple, composable patterns before unnecessary framework complexity.

Connection:

Phase 1 intentionally builds:
- explicit schemas,
- simple retrieval baselines,
- small evaluators,
- transparent experiment runners,

before introducing agent orchestration or learned policies.

## Anthropic: Demystifying Evals for AI Agents

Source:
https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

Key point relevant to this project:

Agent capabilities create evaluation complexity because behavior spans multiple turns, tools, intermediate states, and outcomes.

Connection:

KnowledgeBench separates:
- retrieval metrics,
- future evidence metrics,
- future answer metrics,
- future agent/tool metrics.

This avoids collapsing all behavior into one final-answer score.

## Anthropic: Effective Context Engineering for AI Agents

Source:
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

Key point relevant to this project:

High-signal context matters because model attention is finite.

Connection:

Our later phases should measure not only answer correctness but also:
- retrieved context volume,
- duplicate searches,
- irrelevant evidence,
- retrieval rounds,
- token use.

## Sentence Transformers: Semantic Search

Source:
https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html

Key points relevant to this project:

- semantic search maps queries and corpus items into vector space,
- cosine similarity is a standard retrieval score,
- query/document retrieval can be asymmetric,
- model choice should match retrieval setting.

Connection:

Phase 1 uses all-MiniLM-L6-v2 as a simple dense baseline, not as a claim of state-of-the-art retrieval.

Later phases should evaluate retrieval-specific embedding models and proper query/document encoding when the benchmark is large enough to support meaningful comparison.

## Phase 1 takeaway

The literature supports our direction but does not replace our experiments.

External guidance says BM25, dense retrieval, contextualization, reranking, and rigorous evals can matter.

Our project requirement remains:

```text
measure a failure
before adding complexity to address it
```
