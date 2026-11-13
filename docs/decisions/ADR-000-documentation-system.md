# ADR-000: Documentation System

## Status
Accepted

## Context
This project is both a research project and a learning project. We need to be able to return months later and understand why the system looks the way it does.

## Decision
Use:
- HLD documents for major architecture
- LLD documents for implementation design
- ADRs for important choices
- EXP records for experiments
- glossary entries for learned concepts
- literature notes for papers/articles

## Consequences

### Pros
- Easier learning and interview preparation
- Better reproducibility
- Easier debugging of past decisions

### Cons
- More writing overhead
- Requires discipline

## Current repository workflow (Phase 13 onward)

The repository owner prefers a **single working branch: `main`**.

- Create and update files **directly on `main`** using the connected GitHub file actions.
- Do **not** create feature branches or open pull requests for project experiments.
- Every push should be checked with the repository's push-triggered GitHub Actions workflow; correct test and lint failures on `main`.
- Historical experiment branches may still appear in GitHub and should be deleted through GitHub branch management once their work has been confirmed merged. They are not an invitation to create more branches.

## Experiment documentation checklist

For **every experiment**:
1. Write a numbered `docs/experiments/EXP-XXX-<topic>.md` *before* collecting results: question, hypotheses, controls, inputs/version, seed, metrics, failure criteria, limitations and exact run command.
2. Implement script/module and tests using paths checked against the current repository. Run `uv run pytest`, `uv run ruff check .`, and the experiment driver.
3. Record actual output in a **separate** `docs/experiments/EXP-XXX-<topic>-result.md` (sample counts, numbers, all seeds, negative findings and deviations).
4. Mark unrun or unprovided numerical outputs as **unverified**, never invent them or infer them from passing unit tests.
5. If a result changes architecture or research direction, add/update an ADR and failure taxonomy; maintain links to HLD and research plan.
6. Keep policy-visible inputs distinct from evaluator-only gold. Do not silently reuse an inspected heldout family as pristine after tuning.

For **every phase closeout**:
1. Verify experiment protocols and results, including failures and reproducibility commands.
2. Publish/update the Phase HLD (and LLD where appropriate).
3. Publish architecture decisions (ADRs) and a failure taxonomy as needed.
4. Write a Phase final review: question, results, what was proven, what was not, and remaining work.
5. Update `docs/02-learning-roadmap.md` with status, deliverables, and the next phase's scope.
6. Before Phase 14, ensure the final report and reproducibility index link to the primary evidence.
