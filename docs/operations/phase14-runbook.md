# Phase 14 Runbook — No-Codespace Demo and Audit

## Prerequisites

- Source of truth: [agentic-knowledge-lab](https://github.com/ivedantsharma/agentic-knowledge-lab).
- GitHub Actions is the fallback for running CPU-only tests and demos when GitHub Codespaces is unavailable due to billing. CI uses Ubuntu + Python 3.12 with `uv`.
- The core Phase 14 static and rule-planner pipeline requires **no external embedding/model download at runtime**. The repository's dependency installation may still download packages, and legacy CI audits can use their own dependencies.

## Run without a Codespace

1. Open repository **Actions → CI → newest successful run**.
2. Inspect `Run tests`, `Run Ruff`, `Smoke Phase 14 integrated evidence demo`, `Smoke Phase 14 extractive citation and abstention` and `Audit Phase 14 integrated benchmark development results`. All of these are real CI executions, not simulated.
3. Under that run's **Artifacts**, download `phase14-evidence-demo` if available. Open `phase14_demo.html` in a browser. The page is static and requires no server; source text and question text are HTML-escaped.
4. Read `docs/research/phase14-integrated-development-benchmark-result.md` before interpreting the report. It records the 10/10 fallback diagnostic, 2/6 answerable extraction correctness and the lack of truly unseen evaluation.

## Commands when a Python environment is available

```bash
git clone https://github.com/ivedantsharma/agentic-knowledge-lab.git
cd agentic-knowledge-lab
uv sync --all-groups
uv run pytest
uv run ruff check .
uv run python scripts/run_phase14_integrated_demo.py --strategy static --top-k 5 --extractive-answer
uv run python scripts/run_phase14_integrated_demo.py --strategy auto --question "Where do failed jobs go after retries?"
uv run python scripts/run_phase14_integrated_benchmark.py
uv run python scripts/run_phase14_html_demo.py --output phase14_demo.html
```

Use the exact repository setup command appropriate to the machine. No model weights or network service are required for these Phase 14 scripts once dependencies are installed.

## Quick validation checklist

- The JSON CLI returns `steps` with exact query strings and document IDs.
- Each `evidence` item contains `document_id`, `title`, `source_type`, `effective_at` and a metadata-derived `risk_flag`.
- Unsupported planner intents show `strategy_used=planner_with_static_fallback` and a `fallback_reason`, not an invented answer.
- Base pipeline `answer=null`, status `evidence_only_unverified`; optional `source_answer` is a separate extractive verdict, not world-truth verification.
- For a direct current Borealis question, `--extractive-answer` may produce `every six hours` with source `kbv2-doc-borealis-current`.
- On ambiguous, unanswerable or unsupported intents, abstention is expected. Never interpret a blank answer as proof that retrieved evidence is absent.
- HTML artifact contains actual source citations and HTML-escaped text. Do not infer it is a hosted application.

## What not to conclude

The CPU-only demo doesn't establish modern model planning ability, robust multimodal retrieval, calibrated abstention, source-authority trust, injection safety, or SFT-versus-RL superiority. The hard benchmark tasks were inspected in earlier research phases. Static and auto modes have unequal tool-call budgets.

## How to diagnose common failures

**CI failing on imports:** verify exact package/module paths using the current GitHub repository tree, not memory. The user previously had to correct guessed imports in a Phase 3 runner.

**Ruff error:** inspect its exact file and rule in the run logs, change only the affected code, and recheck tests and Ruff on the new commit.

**Planner fallback on every benchmark case:** expected measured diagnostic for the current hard-v0 corpus. It is not a sign that the benchmark is broken; the historical regex planner has limited coverage.

**No downloadable artifact:** inspect the workflow job's demo generation and upload-artifact steps; do not invent a sandbox download link or assume the artifact exists if a run failed.

**Codespaces remains unavailable:** use the GitHub repository browser for documentation, GitHub Actions for tests and artifacts, or a local Python 3.12 installation when possible. No paid Codespace is essential for reviewing the committed research.

## Next engineering work

To progress from prototype to validated agentic assistant: introduce a real flexible planner with logged tool-call budgets; match static vs planner budget; build provenance/trust checks for current versus pending sources; add matched model answer-generation and citation verification; create independent evaluation families; test abstention and prompt injection end-to-end. This work has NOT been completed by the current demo.
