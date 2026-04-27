---
name: User Profile
description: Who Nick is, his stack preferences, and how he likes to work
type: user
---

Nick builds a PWHL (hockey) stats site as a side project. Comfortable across the full stack — writes Python backend and Svelte frontend himself, asks for help with syntax, architecture decisions, and frontend implementation. Uses uv for Python package management. Runs the backend with `cd backend && uv run uvicorn main:app --reload`. Postgres runs in Docker (`docker start pwhl-stats-db-1`, database name `pwhl`). VS Code is his editor but has trouble with uv-managed venv interpreter detection — the Python Environments extension (ms-python.vscode-python-envs) is the right fix.
