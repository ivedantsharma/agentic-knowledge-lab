# EXP-115 — Discounted Returns and Finite-Horizon Oracle Baselines

## Research question

With Reward v2 validated in EXP-113/114, does the finite retrieval
environment admit a meaningful reward-aware action choice, and how does
credit assignment change when future rewards are discounted?

## Hypotheses (defined before the run)

1. On the grounded Cirrus case, the hidden-label oracle should choose
   SEARCH_K2 → STOP, collecting the rank-2 authoritative document without
   paying for unnecessary documents ranked 3–5.
2. With gamma=1, staged retrieval and direct retrieval to the same final K
   have the same *undiscounted* return because per-document rewards/costs
   are incremental and repeated support is not rewarded.
3. With gamma=0.9, actions' timing changes G0 and tends to favor recovering
   useful evidence earlier; this does **not** substitute for measured latency.
4. If supporting evidence lies beyond maximum K=5, no policy can attain
   full evidence coverage. For the synthetic rank-6 case, an oracle should
   prefer STOP_NOW to unnecessary searches under this reward.

## Protocol

- Reuse the EXACT frozen EXP-111/112 Cirrus ranking and benchmark route-003
  gold label, verified against the repository's documents/tasks.
- Reuse the three explicitly **synthetic** EXP-114 stress configurations.
- Enumerate terminal trajectories under strictly increasing K in {1,2,3,5}
  and STOP, with a default step cap of 6.
- Calculate G0 = sum_t gamma^t * r_t for gamma in {1.0,0.9}.
- Compare gold-aware diagnostic oracle to six fixed, gold-blind strategies:
  STOP_NOW, FIXED_K1/2/3/5 and ESCALATE.
- Break equal-score oracle ties by fewer retrieved documents and fewer
  actions. Gold labels appear only in evaluator/oracle code.
- Record return, evidence coverage and retrieval cost separately.

No trained policy, model inference, new retrieval ranking, or answer
generation is involved.

## Distinctions and failure modes

- An oracle is a label-aware diagnostic **upper bound**, not a deployment
  policy and not evidence that an LLM learned anything.
- Evidence coverage is not answer correctness; conflicting-document exposure
  remains a separate diagnostic, never an automatic negative reward.
- With no per-action cost, an undiscounted reward can tie strategies that
  use different numbers of steps. Discounting changes optimization
  incentives, but does not quantify wall-clock latency.
- The fixed rank-ID observation lacks document text, confidence and
  evidence-verification signals. Improving policy observability may be
  necessary before a real learned continuation/STOP policy can generalize.
- Synthetic stress cases are not held-out knowledge-benchmark results.
- We do not aggregate one grounded and three synthetic cases as though
  they were a real-world evaluation distribution.

## Run

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_phase12_return_oracle_baselines.py
```

## Acceptance criteria

- Every legal trajectory is evaluated once, and truncated paths are rejected.
- Invalid gamma values are rejected; gamma=1 preserves undiscounted returns.
- Fixed-policy choices contain no gold labels.
- Oracle return is not worse than any evaluated fixed-policy return under
  the same horizon/discount.
- Rank-6 stress case is identified as unreachable, never misreported as
  task success.

## Next step

Proceed to a stochastic policy/exploration baseline with strict separation
between policy-visible features and evaluator-only hidden labels. Add
source-family held-out evaluation before claiming learned improvements.
