# Phase 13 Research Campaign Plan — Preregistered Order

## Central question
Which knowledge architectures and control strategies improve **grounded task success** on difficult knowledge benchmarks, under reproducible resource budgets and with evidence-family generalization?

## Scope
Existing corpus contains 22 KnowledgeBench v2 hard documents, 12 paired routing questions across six source families, and Phase 11's 17 measured policy examples. These are *development-scale materials*, not a new untouched heldout dataset. Phase 13 must avoid optimizing on already inspected families and falsely declaring external generalization.

## Initial experiment matrix

| Gate | Study | Independent variable | Controlled variables | Primary metrics | Key failure criterion |
|---|---|---|---|---|---|
| EXP-120 | Corpus, task and protocol registry | Input/source provenance | Existing files and no performance tuning | SHA-256, counts, family/split exposure, missing data | Untracked provenance or split overlap |
| EXP-121 (planned) | Fixed retriever baselines under one protocol | BM25 vs Dense vs Hybrid | Corpus, tasks, K, metric, seed, query text | supporting Recall@K, MRR, cost | Previous ranking configuration changes unnoticed |
| EXP-122 (planned) | Knowledge representation ablation | Flat vs hierarchy vs graph/claim | Evaluation set, quality measures, retrieval budget | evidence success, trace length, latency | Representation confounded with retrieval budget |
| EXP-123 (planned) | Agentic vs static retrieval | Rule/fixed vs planner | Same tool interface, task families, max calls | grounded answer accuracy, calls, errors | Oracle leakage or over-broad context |
| EXP-124 (planned) | Learned policy generalization (only after fresh families) | Fixed K3 vs SFT vs RL with shared action/state | Common retriever, action semantics, training split, compute and quality | return, completion, answer accuracy, variance | Models use different protocols or tainted test set |
| EXP-125 (planned) | Robustness/abstention and failure study | Distractors, stale/pending, injections, unanswerable | Same policy checkpoints and threshold protocol | accuracy, abstention, source quality, attack success | Improved metric achieved by refusing everything |

**Numbers and order after EXP-120 are working plan identifiers, not claims of completed experiments.** Each study gets its own hypothesis/protocol, actual measured result, errors, limitations and next decision.

## Frozen data and split policy
- EXP-118 evaluated (and exposed during design) Borealis, Solstice, Meridian, Nimbus and Orion; no longer pristine for iterative policy tuning.
- Cirrus was EXP-117/118 training. Phase 11's heldout included Meridian, but Phase 12 heldout included that family too.
- Do not invent new independent families through relabeling or paraphrasing old evidence.
- To support new learned-policy generalization claims, source independent documents/tasks and freeze family-disjoint test IDs **before** fitting/tuning.
- Gold answer and support IDs may appear in evaluator metadata, never policy observation.
- Prefer source-family bootstrap or family-level intervals rather than treating paraphrases as independent.

## Experiment template
Use `docs/experiments/EXP-TEMPLATE.md` and a separate `-result.md` after actual driver runs. Record source hashes, environment, controls, sample counts, seed, uncertainty, all relevant baselines, failure cases, negative evidence and exact reproduction commands.

## Decision gates
Do not promote a learned policy unless it improves heldout answer-quality / evidence completeness beyond strong fixed baselines at comparable cost, across independent seeds and new families. Promote *negative findings* and architecture limitations into ADRs. Do not assume higher model scale yields retrieval improvement.

## Next task
EXP-120 provenance gate is complete (390 tests at initial closeout; EXP-121 CI now 400 tests). EXP-121 is complete: observed BM25/Dense/Hybrid K1/2/3/5 metrics match earlier K3 results, with Hybrid vs BM25 MRR@3 +0.0139 and descriptive family-bootstrap interval [−0.1111,+0.1250]. EXP-122 has started with a preregistered common-substrate feasibility gate: Phase 5 hierarchical and Phase 6 graph benchmarks use different task sets and cannot be directly compared; run the source/label parity audit before designing matched-representation ablations.

## EXP-122 Gate B1 update — verified source parity

Gate A found zero shared Phase 5/Phase 6 benchmark questions, so their historical percentages remain incomparable. The Phase 6 native graph and its four existing multi-hop questions now serve as a **single development-only** source for the next controlled ablation. The lossless source bridge preserved 15 claim evidence references as 15 flat evidence units and 15 sections across 11 entity-grouped hierarchy documents. The graph retains its 15 source claims. CI passed 416 tests, Ruff and both source-provenance steps.

Gate B2 (still pending) must compare actual flat, hierarchical and graph implementations under matched evidence/context budget and separately report gold-claim retrieval versus answer correctness, call count, and provenance. Because this set was graph-designed, no claim of external cross-representation generalization is permitted. **EXP-122 completed as a four-question system-level development comparison** (not a pure causal representation ablation): Flat BM25 0.6250 mean evidence coverage / 1 of 4 fully complete; hierarchy 0.7500 / 2 of 4; native graph 1.0000 / 4 of 4. Output cap was 3 source evidence atoms; graph-oriented questions and different ranker/model paths prevent causal or external-validity claims. Full user-provided numerical results archived in `docs/experiments/EXP-122-knowledge-representation-ablation-result.md`. **Phase 13 is 3/6 core studies complete (50%), three remaining.** EXP-123 has completed its full real-MiniLM five-question development evaluation (432 tests passed in the implementation CI): static top3 Recall 0.8000 / full-evidence 3/5; static top9 Recall 1.0000 / full-evidence 5/5; static repeat top3 Recall 0.8000 / full-evidence 3/5; rule-agent Recall 0.8000 / full-evidence 4/5 and a pre-search OOD failure on 1/5. Query planning helped familiar tasks but did not beat one-shot top9, and the old template-based planner failed on novel intent. Exact results and limitations are archived in `docs/experiments/EXP-123-static-vs-agentic-search-result.md`. **Four of six planned Phase 13 experiments are now complete (~67%); EXP-124/125 and the final phase review remain.** The static top3/top9/repeated-top3 controls separate exposed evidence budget from search calls, and the RuleBasedPlanner can use up to three dependent searches. Results must be interpreted as development traces, not new-family generalization.
