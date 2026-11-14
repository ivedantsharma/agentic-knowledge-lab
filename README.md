# Agentic Knowledge Lab

Research-engineering experiments on **agentic search, knowledge representations, evidence grounding, and evaluation**. The repository contains reusable retrieval and grading implementations, reproducible research protocols, a small evidence-first integration demo, and a record of positive, negative, and inconclusive findings.

> **Research scope:** This is a development-stage system, not a production-ready fact-checker. The known benchmark families have been inspected across experiments; no broad unseen-family generalization is established.

## What is implemented

- **Retrieval:** BM25, MiniLM Dense, Hybrid reciprocal rank fusion, reranking, structure-aware chunks, hierarchical and claim-graph methods.
- **Agents:** multi-hop planning, query observations, tool traces, static-query fallback and evaluation of stopping/failure behavior.
- **KnowledgeBench:** typed multi-hop, distractor, contradiction, stale, ambiguity and unanswerable tasks; evidence/retrieval/trace/grounding graders.
- **Learning research:** supervised action-classification and REINFORCE prototypes, fair-baseline and protocol-compatibility studies. **No supported learned SFT-versus-RL superiority claim.**
- **Phase 14 integration:** a common BM25/Dense/Hybrid ranking interface, a transparent rule planner with original-question fallback, source provenance and risk flags, an opt-in narrow source-cited extractive answer/abstain gate, JSON and portable HTML demonstrations.

## Try the evidence-first demo

The default BM25 integration does **not** need model weights or a GPU. With Python 3.12 and `uv` installed:

```bash
uv sync --all-groups
uv run pytest
uv run ruff check .

# Explainable evidence JSON with provenance and fallback traces
uv run python scripts/run_phase14_integrated_demo.py --strategy static --top-k 3

# Opt-in narrow extractive answer and source citations
uv run python scripts/run_phase14_integrated_demo.py --strategy static --top-k 5 --extractive-answer

# Unknown intent: original-question fallback
uv run python scripts/run_phase14_integrated_demo.py --strategy auto --question "Where do exhausted failed jobs go?"

# Model-based retrieval (downloads frozen MiniLM when selected)
uv run python scripts/run_phase14_integrated_demo.py --backend hybrid --strategy static --top-k 5

# Development benchmark + standalone HTML report
uv run python scripts/run_phase14_integrated_benchmark.py
uv run python scripts/run_phase14_html_demo.py --output phase14_demo.html
```

Alternatively, open [GitHub Actions](https://github.com/ivedantsharma/agentic-knowledge-lab/actions), choose a successful CI run, and download the **`phase14-evidence-demo`** artifact. Its HTML opens locally without a web service or Codespaces.

**Answer integrity:** The base pipeline always has `answer=null` and `status=evidence_only_unverified`. With `--extractive-answer`, a *separate* `source_answer` may be returned for a few directly named service questions backed by explicit source-manual text; it abstains on unsupported or conflicting evidence. Such extracted values are **not independently verified world facts**.

## Selected observed research results

| Study | Development-scale result | Limitation |
|---|---|---|
| EXP-121 | Hybrid MRR@3 0.8333 vs BM25 0.8194; six-family bootstrap interval for the difference spans zero | No established universal Hybrid win |
| EXP-122 | Graph retrieval covered 4/4 graph-derived task evidence paths; flat 1/4, hierarchy 2/4 | Graph-aligned tasks; different algorithms, not causal proof |
| EXP-123 | Rule agent recovered full evidence on 4/5 but failed before searching on the OOD fifth; static Top9 recovered 5/5 | Unmatched call/document budgets |
| EXP-124 | Common BM25 policy execution protocol and fixed-K baselines validated | Learned SFT/RL comparison **stopped inconclusive** |
| EXP-125 | Hybrid Recall@5 0.8889 with 5/6 complete evidence chains; labeled risk documents also exposed at K5 | Retrieval-only, not answer quality or injection safety |
| Phase 14 | On 10 inspected tasks, source-extractive answers correct 2/6 answerable, abstained 4/4 unanswerable; auto fallback **10/10** | Narrow extractor; planner not generalized; unmatched call budgets |

The measured Phase 14 results deliberately expose **negative findings**, not just successes. Source-grounded extraction currently has limited answer coverage, and the historical rule planner needs fallback for all ten hard-v0 tasks.

## Documentation

- [Phase 13 final research review](docs/research/phase13-final-review.md)
- [Phase 14 HLD](docs/architecture/phase14-hld.md) and [LLD](docs/architecture/phase14-lld.md)
- [Phase 14 integrated development benchmark result](docs/research/phase14-integrated-development-benchmark-result.md)
- [Phase 14 engineering handoff review](docs/research/phase14-integration-handoff-review.md)
- [Phase 14 no-Codespace runbook](docs/operations/phase14-runbook.md)
- [Portfolio research-engineering case study](docs/portfolio/agentic-knowledge-lab-case-study.md)
- [Learning and project roadmap](docs/02-learning-roadmap.md)

**Data integrity:** The separate `EXP-124-illustrative-hypothetical-simulation-NOT-RESULTS.md` contains deliberately fictional teaching-only numbers. They are **not experimental findings** and must never be quoted as actual model outcomes.

## What remains open

Truly independent source-family evaluations; a general grounded answer generator and verifier; calibrated abstention and prompt-injection resistance; robust non-template agent planning; fair same-budget latency/quality comparisons; compatible trained SFT/RL inference checkpoints; production deployment.

We don't add complexity for its own sake. Every addition needs a baseline, a measurable research question, source provenance, and honest failure analysis.
