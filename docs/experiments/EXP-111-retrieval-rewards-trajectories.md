# EXP-111 — Retrieval Rewards and Trajectories

## Question
Can a deterministic environment distinguish an incomplete early stop from an evidence-complete continuation, accounting for incremental retrieval cost?

## Setup
- Same 22-document hard KnowledgeBench corpus as Phase 10.
- Same BM25 + MiniLM dense + RRF ranking.
- Fixed query: `route-003`, a Cirrus retry question (EXP-107 observed supporting evidence first at k=2).
- Two preselected trajectories from the same initial state and fixed ranking.
- No model learning and no policy gradients yet.

## State and observation
The policy sees the query, previously retrieved document IDs, the current requested top-k, number of steps and whether the episode is done. It cannot see gold supporting-document IDs.

## Actions
`SEARCH_K1`, `SEARCH_K2`, `SEARCH_K3`, `SEARCH_K5`, and `STOP`. Search must increase k. Gold labels are used by the evaluator only.

## Reward (initial design; to be stress-tested)
- +2 per *newly* retrieved supporting document
- -0.1 per *newly* retrieved document
- +1 for stopping with all gold supporting documents retrieved
- -1 for stopping before full supporting coverage

This deliberately measures *evidence coverage*, not factual answer correctness or evidence freshness. Unanswerable tasks, query reformulation, alternative strategies, real latency, and generated answers are out of scope. Missing the maximum step count ends the episode without an extra stop reward/penalty, a limitation for the next reward-design audit.

## Expected diagnostic
`SEARCH_K1 → STOP` should be worse than `SEARCH_K1 → SEARCH_K2 → STOP` when supporting evidence first appears at rank 2. This tests a reward/trajectory mechanism, not model intelligence.

## Next
Stress-test reward incentives and termination; compare reward to meaningful outcomes; then introduce stochastic policies, credit assignment, returns, and policy gradients. Do not train Qwen on this tiny environment yet.
