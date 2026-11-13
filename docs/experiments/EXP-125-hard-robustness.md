# EXP-125 — Hard Knowledge Retrieval Robustness and Abstention Boundaries

## Status
**Preregistered before EXP-125 evaluation.** EXP-124 learned-policy comparison remains blocked by incompatible action/observation/retrieval protocols and lack of genuinely new families. EXP-125 is an **independent, development-only robustness diagnostic**, not an SFT-versus-RL comparison.

## Research question
On the same hard KnowledgeBench v2 tasks and evidence source, how do fixed BM25, Dense MiniLM, and Hybrid RRF differ in gold-support retrieval versus exposure to stale, contradictory, distracting or ambiguous documents as K increases? What is *not* measurable without an answer/abstention controller?

## Frozen sources
- `data/processed/knowledgebench_v2_hard_documents_v0.json`: full 22-document hard corpus.
- `data/processed/knowledgebench_v2_hard_tasks_v0.json`: existing hard v0 tasks, with evaluator-only support, conflicting, stale, distractor, ambiguity and should-answer annotations.
- `data/processed/phase9_prompt_injection_pairs_v0.json`: previously authored paired injection cases. Inventory their count and source hash but **do not score attack success without running an actual model on clean vs injected evidence**.

## Preregistered systems
- BM25: existing `BM25Retriever` using all source documents.
- Dense: `sentence-transformers/all-MiniLM-L6-v2`, cosine similarity, frozen weights.
- Hybrid: existing reciprocal-rank fusion `rrf_k=60` from BM25 and Dense *full-corpus rankings*.
- Common input: unchanged question, no oracle query rewriting, no post-hoc reranking, same corpus.
- K values: **1, 3, 5**. Higher K may improve recall while increasing misleading evidence exposure.

## Primary metrics
1. Mean supporting Recall@K on **answerable** tasks and fraction with all gold support within K; mean Reciprocal Rank@K.
2. For each label type (distractor, contradiction, stale), the **conditional exposure rate** among tasks that actually have that label. Report denominator, not a misleading global average.
3. On ambiguous tasks, fraction of marked ambiguity candidates retrieved; **not** a claim that the query was disambiguated.
4. Unanswerable task count and fraction with nonempty retrieval results. **This is NOT abstention accuracy**: a retriever returning documents is not claiming an answer.
5. Per-task retrieved IDs, coverage and risk flags so any error is traceable.

## Controls and forbidden conclusions
- Test cases were written/inspected in earlier phases, so **do not** claim fresh-family generalization.
- Gold documents and challenge labels are evaluator-only, never appended to candidate retrieval queries or their scoring inputs.
- Retrieving a contradiction/stale document is an **exposure risk**; without a downstream answer generator we cannot conclude that it was believed or used in an answer.
- Do not award a retriever perfect unanswerable detection just because a nonempty result set exists; no answer/abstention module participates.
- Existing Phase 9 injection case count is **provenance inventory only**. No model-based clean/injected attack score without paired inference.
- No unmeasured cost/latency, confidence intervals from tiny related groups, policy generalization, or artificial heldout re-labeling.

## Acceptance
- Frozen source hashes and document/task reference integrity verified before retrieval.
- Three rankers evaluated on identical questions, K=1/3/5, with results independently graded against task labels.
- K monotonic support recall; risk exposure measured separately. Per-task evidence and conditional sample counts reported.
- The result record is not declared complete until the real MiniLM experiment output has been observed and archived.

## Implementation and experiment outputs
- Runner: `scripts/run_phase13_hard_robustness_comparison.py`
- Independent grader: `knowledgebench/evaluation/phase13_hard_robustness.py`
- Tests: `tests/test_phase13_hard_robustness.py`
- Result: `docs/experiments/EXP-125-hard-robustness-result.md`

Reproduce:
```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_hard_robustness_comparison.py
```

## Phase 13 progress
Four full experiments (EXP-120–123) completed = **4/6 (~67%)**. EXP-124 is blocked at its compatibility gate. EXP-125 is starting. A measured EXP-125 result alone does **not** close EXP-124 or the Phase 13 final research review.
