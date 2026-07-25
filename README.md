# chat-memory-intelligence — M1 Minimal scaffold

This repository contains a minimal scaffold for milestone M1 (memory write path).

Run tests with:

```bash
python -m pip install -r requirements.txt
pytest -q
```

## Progress log

- M4 — Observability plane: completed (tests `tests/test_observability.py` passed). — 2026-07-25
- M5 — Governance (audit log, deletion, explainability): completed (tests `tests/test_governance.py` passed). — 2026-07-25
- M6 — Economics (cost-per-useful-memory): completed (tests `tests/test_economics.py` passed). — 2026-07-25
- M7 — CI/CD for AI (eval gate, shadow mode): completed (tests `tests/test_eval_gate.py` passed). — 2026-07-25
- M8 — Human-in-the-loop (corrections, forget command): completed (tests `tests/test_hitl.py` passed). — 2026-07-25
- M9 — Continuous learning (reflection, conflict resolution): completed (tests `tests/test_reflection.py` passed). — 2026-07-25

## Setup & Run (cross-platform)

Prereqs: Python 3.10+ and Git.

1) Create an isolated environment and install dependencies

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) Run tests

```bash
pytest -q
```

3) Quick demo (extract → evaluate → store)

Run the simple demo:

```bash
python demo_run.py
```

Or the comprehensive demo showing all features (extract, retrieve, correct, forget, reflection):

```bash
python demo_full.py
```

4) Connecting an LLM (optional)

- Add an API key as `OPENAI_API_KEY` (or the provider env var your client requires).

Windows (PowerShell):

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

macOS / Linux:

```bash
export OPENAI_API_KEY="sk-..."
```

Implement a small client (example file `src/memory/llm_client.py`) and call it from
`src/memory/evaluator.py` to replace the heuristic evaluator. Keep calls deterministic
(temperature=0) for eval/reproducibility and wrap calls in timeouts for reliability.

5) CI

This repo includes a GitHub Actions workflow at `.github/workflows/eval-gate.yml` that runs
`pytest`, `ruff`, and `mypy` on push/PR to `main`/`master`.

6) Notes & next steps

- Heuristic logic lives in [src/memory/extractor.py](src/memory/extractor.py) and [src/memory/evaluator.py](src/memory/evaluator.py).
- The golden-set harness is at [src/memory/eval_harness.py](src/memory/eval_harness.py) and tests/data/golden_set.jsonl
- For production: consider async model calls, circuit-breakers, RLS for user scoping, and secure storage of keys.

