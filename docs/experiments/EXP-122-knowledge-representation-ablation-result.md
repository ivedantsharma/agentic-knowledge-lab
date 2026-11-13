# EXP-122 Result — Paired Representation System Comparison

## Status and research decision

**EXP-122 complete as a small, paired development-stage SYSTEM comparison; a pure causal representation-only ablation and unseen-family validation remain unproven.** The original Phase 5-vs-Phase 6 benchmark comparison was correctly blocked in Gate A; Gates B1 and B2 created and evaluated a common source representation without inventing independent examples.

### Research question

On the same existing Phase 6 graph-derived four questions and evidence source, how much relevant evidence is retrieved by a flat lexical system, a hierarchical Dense+CrossEncoder system, and native claim-graph QA when output is capped at three evidence atoms?

## Gate A — Historical protocols are incomparable

The user executed `uv run python scripts/run_phase13_representation_substrate_audit.py`.

| Property | Phase 5 hierarchy source | Phase 6 graph source |
|---|---:|---:|
| Structured documents | 6 | — |
| Sections | 9 | — |
| Entities | — | 11 |
| Claims | — | 15 |
| Tasks | 3 | 4 |
| Shared exact task IDs/questions/answers | **0** | **0** |

Gate A found `complete_paired_task_crosswalk=False`. The historical Phase 5 evidence retention and Phase 6 graph answer accuracy must not be compared directly.

Source fingerprints:
- Phase 5 documents: `a66964b95752fc8bb50a1c2789c548d4618cd33145c4962adbdb2a9937c21d89`
- Phase 5 tasks: `6f77a40b281a9c8d3e424e2d44be4a7236829eb9b37612a549123aca89a5e5dc`
- Phase 6 graph: `4e3b26bd9dfbc57f57eb501132279f50e96be87e7db96ba7838d552a2669718e`
- Phase 6 graph tasks: `767c9b0b2a3ea42d3d08407e1d095062790f770917d1e2452632adc5c9f0db9e`

## Gate B1 — Common data contract

The original Phase 6 graph claims were projected losslessly into three views:
- Flat: **15** source evidence atoms, with relation labels.
- Hierarchy: **11** subject-grouped documents with **15** evidence sections.
- Graph: the original **15** claims, relationships, and evidence references.

All **four existing graph-derived QA questions** are identical for the three approaches. Exact evidence text and source provenance were preserved. No newly gathered families or untouched holdout were introduced.

GitHub CI run `43499979668`: **416 tests passed**, Ruff passed, source contract and EXP-120 provenance audit passed.

## Gate B2 — Preregistered observed numerical comparison

The user executed:
```bash
uv run python scripts/run_phase13_paired_representation_comparison.py
```

The MiniLM weights (103 objects) and cross-encoder weights (105 objects) loaded. The Hugging Face unauthenticated-request warning did not prevent the run.

**Controls:** 4 source questions, 15 evidence atoms, at most 3 evidence atoms returned per question. Flat uses existing BM25, hierarchical uses the existing coarse-to-fine Dense+CrossEncoder retriever with all 11 parents eligible, and graph uses native explicit-entity ClaimGraphQA with semantic path ranking. Original gold claim IDs and answers are accessed by the evaluator *after* retrieval, not provided as policy inputs.

### Per-task findings

| Task | Gold claims | Flat BM25 coverage | Hierarchy coverage | Graph coverage | Full evidence recovered (Flat / Hierarchy / Graph) |
|---|---:|---:|---:|---:|---|
| graph-001 | 3 | 0.3333 | 0.3333 | 1.0000 | No / No / Yes |
| graph-002 | 2 | 0.5000 | 1.0000 | 1.0000 | No / Yes / Yes |
| graph-003 | 3 | 0.6667 | 0.6667 | 1.0000 | No / No / Yes |
| graph-004 | 2 | 1.0000 | 1.0000 | 1.0000 | Yes / Yes / Yes |

### Aggregates

| Metric | Flat BM25 | Hierarchy | Native graph |
|---|---:|---:|---:|
| Mean gold claim coverage | **0.6250** | **0.7500** | **1.0000** |
| Tasks with all gold evidence | **0.2500 (1/4)** | **0.5000 (2/4)** | **1.0000 (4/4)** |
| Mean retrieved evidence atoms | 3.0000 | 3.0000 | 2.5000 |
| Mean returned text words | 34.7500 | 38.7500 | 35.0000 |
| Reported candidate scoring counts | 15.0000 | 29.0000 | 2.0000 |
| Native answer exact match | Not evaluated | Not evaluated | 1.0000 (4/4) |
| Native graph claim-path exact match | Not evaluated | Not evaluated | 1.0000 (4/4) |

**Do not compare candidate counts as if they were the same unit.** Flat counts document BM25 scores, hierarchy sums scored parents/sections/chunks, while graph reports candidate path ranking count (not all graph processing work). None provides a controlled wall-clock latency measure.

### Per-task raw resource diagnostics

| Task | Flat atoms / words / candidates | Hierarchy atoms / words / candidates | Graph atoms / words / candidates |
|---|---|---|---|
| graph-001 | 3 / 33 / 15 | 3 / 36 / 29 | 3 / 42 / 3 |
| graph-002 | 3 / 33 / 15 | 3 / 44 / 29 | 2 / 32 / 2 |
| graph-003 | 3 / 36 / 15 | 3 / 34 / 29 | 3 / 39 / 2 |
| graph-004 | 3 / 37 / 15 | 3 / 41 / 29 | 2 / 27 / 1 |

Graph QA answered and selected gold paths correctly on all four tasks. Its answer accuracy is **not** comparable with flat and hierarchy because the latter did not generate answers.

## Validation

- Latest Gate B2 implementation CI: GitHub Actions run `43501815415`, commit `523e02bfd5ca3ced97881fe53effc5601dd29c60`.
- **423 tests passed in 17.24s**, Ruff passed, EXP-120 source-provenance audit passed, and EXP-122 common representation contract passed.
- Tests include source atom preservation, exact task-path integrity, capped evidence outputs, fake-model system integration, and evaluator gold-label isolation.
- Full pretrained-model numerical results above are directly from the **user's local experiment run**, not inferred from CI smoke tests.

## Failure analysis and limitations

1. **Multi-hop gap:** graph-001 and graph-003 require three connected facts; at K3 both flat and hierarchy miss at least one claim, while graph QA follows a complete path.
2. **Hierarchy helps some queries:** hierarchy recovers both claims on graph-002 versus flat coverage 0.5, but still misses multi-hop chain evidence elsewhere.
3. **Graph-favorable benchmark:** the original Phase 6 graph and questions were designed together; representational edge access and task alignment favor graph.
4. **Retriever/model confound:** BM25 vs dense+cross-encoder vs semantic graph-path scoring differ, as do explicit edge navigation and response generation. This is *not* a controlled one-variable causal ablation of representation alone.
5. **Cost confound:** a three-atom output cap aligns exposed evidence units but not model inferences, indexing work, retrieval latency, or compute.
6. **No broad inference:** four questions from one existing graph source; no independent evidence-family variation, meaningful confidence intervals, novel deployment corpus, or untouched test set.
7. **Answer-quality asymmetry:** native graph outputs answers; flat and hierarchy do not. Retrieval completeness alone is not final-answer correctness.

## Scientific conclusion

**Supported:** On the four existing graph-oriented tasks and this output budget, native graph QA achieves full evidence-path retrieval (4/4) and exact native answer/path accuracy (4/4). Hierarchy achieves 2/4 full evidence coverage; flat BM25 achieves 1/4. All measurements are reproducible and documented.

**Not supported:** graph representation alone causes the difference; graph wins on new domains; graph uses fewer compute resources; flat/hierarchy have worse end-to-end answer accuracy; RL/agentic policies outperform baselines.

**Decision:** Close the EXP-122 *system-level* development study and retain its confound limitations as first-class research findings. A separate, more rigorous representation-only ablation would require common scorer/reasoner access and new source-independent cases. Move to EXP-123: agentic versus static search, with an explicit shared tool protocol and budget. See `docs/architecture/ADR-018-representation-ablation-evidence-parity.md` for the durable architectural decision and limitations.

## Reproduce

```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase13_representation_substrate_audit.py
uv run python scripts/run_phase13_common_representation_contract.py
uv run python scripts/run_phase13_paired_representation_comparison.py
```
