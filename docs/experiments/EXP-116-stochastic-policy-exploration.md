# EXP-116 — Stochastic Policy and Exploration (No Training)

## Question

What happens when a retrieval policy must choose SEARCH_K1/K2/K3/K5 or
STOP with incomplete observations and stochastic exploration, rather
than using evaluator gold labels to select optimal actions?

## Preregistered expectations

1. With epsilon=0, a target-K2 policy equals the EXP-115 fixed-K2
   policy on the grounded Cirrus task (return +2.80, coverage 1).
2. With epsilon=1, choices are uniform among currently legal actions;
   observed episode returns vary and multiple trajectories appear.
3. An epsilon=0.2 target-K2 policy and target-K5 policy trade off
   unnecessary retrieval versus missing late support.
4. With max_steps=6, no **legal** retrieval episode can time out:
   there are at most four strictly increasing search actions followed
   by STOP (five total steps). With max_steps=2, some stochastic
   episodes should time out, exercising Reward v2.
5. Holding the question/ranking/seed/policy fixed while changing hidden
   support labels cannot alter sampled policy actions, although
   rewards and evaluator metrics change.

## Environment / methods

- Reuse the EXP-111 frozen top-five Cirrus ranking and verified
  route-003 gold supporting ID as the one grounded evaluation case.
- Reuse EXP-114's three explicitly labeled **synthetic** support variants;
  they are sensitivity probes, not held-out evidence-family benchmarks.
- Use Reward v2, with gamma=0.9 for discounted return reporting.
- Compare three reward-blind policies:
  - UNIFORM: epsilon=1.0, uniform among legal actions
  - EPS_K2: K2 as target, epsilon=0.2
  - EPS_K5: K5 as target, epsilon=0.2
- Sampling is seeded, with 400 on-policy episodes per
  case × policy × horizon configuration.
- Evaluate max_steps in {2,6} and report mean discounted return,
  sample return standard deviation (population SD), oracle gap,
  mean evidence coverage, completion rate, premature STOP rate,
  timeout rate, documents retrieved, conflicting-document exposure
  and distinct action trajectories.
- Oracle labels are used for the diagnostic ceiling and scoring only.
  The policy function receives only `RetrievalObservation` and `Random`.
  No reward or hidden supporting ID is an argument to the policy.

The stochastic policy does not update its parameters, so this is
**not a policy-gradient, Q-learning, or learned-agent experiment**.

## Definitions

- Epsilon exploration: with probability epsilon choose uniformly from
  all legal actions, and otherwise choose the target action if legal;
  once target is no longer legal, default to STOP.
- Action masking: remove illegal repeat or decreasing search budgets,
  and forbid choices after episode termination.
- On-policy rollout: actions are sampled using the same policy being
  evaluated, not copied from gold-oracle trajectories.
- Completion: all evaluator supporting IDs appear in retrieved IDs;
  this is *not* proof of correct final answers.
- Premature STOP: explicit STOP without complete supporting evidence.
- Timeout: terminal action other than STOP, when the configured
  episode step cap is reached.
- Oracle gap: gold-aware optimal discounted return minus sampled
  mean discounted return under the same cap and gamma.

## Important limitations

- The current policy observation contains document IDs but no
  retrieved document text, semantic confidence, evidence entailment,
  source recency or contradiction judgments.
- Some synthetic cases have **identical** visible questions and
  rankings but different hidden support labels. No observation-only
  policy can perfectly identify the appropriate budget across these
  indistinguishable cases.
- Observed MC differences have sampling variance; exploratory trends
  are not evidence of policy learning or generalization.
- Reward remains a proxy for gold-document presence and retrieval
  cost, not answer correctness or safe contradiction handling.
- The default six-step timeout is currently unreachable with legal
  choices. This is an action-space/horizon design limitation, not a
  reason to relax the EXP-113/114 reward tests.

## Validation

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_phase12_stochastic_policy_exploration.py
```

## Next gate: EXP-117

Introduce a minimal tabular policy-gradient learner (REINFORCE) on
frozen, controlled environments, with multiple random seeds, initial
and post-training performance, gold isolation, and comparisons against
uniform/fixed budget baselines. Do not claim generalization until
training/evaluation evidence families are held out and varied.
