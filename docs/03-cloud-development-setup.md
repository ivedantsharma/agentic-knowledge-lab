# Cloud Development Setup

This project is designed to work without local Git, Python, Codex, or VS Code installation.

## Primary development environment

We use **GitHub Codespaces**.

A Codespace is a cloud computer attached to this repository. It gives us:
- a VS Code-like editor in the browser,
- a terminal,
- Git,
- Python,
- extensions,
- package installation,
- port forwarding,
- and a reproducible Linux environment.

Your corporate laptop acts mainly as a browser.

## Mental model

GitHub repository
↓
Codespace cloud machine
↓
edit / run / test
↓
commit
↓
push
↓
GitHub repository

## Open a Codespace

1. Open the repository on GitHub.
2. Click the green **Code** button.
3. Click the **Codespaces** tab.
4. Click **Create codespace on main**.
5. Wait for the browser editor to load.

## Open a terminal

Inside Codespaces:

1. Click **Terminal** in the top menu.
2. Click **New Terminal**.

The terminal should start inside the repository, usually at a path like:

```text
/workspaces/agentic-knowledge-lab
```

## First commands

### Where am I?

```bash
pwd
```

### What files are here?

```bash
ls
```

### Check Git

```bash
git status
```

### Check Python

```bash
python --version
```

If `python` is unavailable, try:

```bash
python3 --version
```

## uv

We use `uv` to manage Python versions, dependencies, and the project virtual environment.

Check whether it exists:

```bash
uv --version
```

If not, install it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then open a new terminal and run:

```bash
uv --version
```

## Create/sync the project environment

```bash
uv sync
```

This creates an isolated `.venv` environment for the project.

## Verify the project

Run the starter script:

```bash
uv run python scripts/hello.py
```

Expected output:

```text
Agentic Knowledge Lab is alive.
```

Run tests:

```bash
uv run pytest
```

Expected initial result:

```text
1 passed
```

Run linting:

```bash
uv run ruff check .
```

## Git workflow

### See changes

```bash
git status
```

### See exact line changes

```bash
git diff
```

### Stage changes

```bash
git add .
```

### Commit

```bash
git commit -m "Describe the change"
```

### Push

```bash
git push
```

## Security

Never commit real API keys.

Later, real secrets should live in `.env` or Codespaces secrets.

The repository contains `.env.example` only as a template.
