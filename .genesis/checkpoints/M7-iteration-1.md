# M7 — CI Eval Gate (iteration 1)

Status: kickoff

Goals for iteration 1:
- Create an evaluation gate harness that can run a golden-set of queries and measure retrieval precision/recall.
- Add a placeholder test (`tests/test_eval_gate.py`) so the repo has a canonical demo command for the verifier: `pytest tests/test_eval_gate.py -q`.
- Define the golden-set data format (JSONL) and a minimal runner API `src/memory/eval_harness.py` (planned).

What I did now:
- Added `tests/test_eval_gate.py` placeholder.
- Created this checkpoint and updated `CURRENT.md` to mark M7 active_loop.

Next steps:
- Implement `src/memory/eval_harness.py` to run golden-set queries against the `retrieve_for_user()` API and compute precision/recall.
- Add a small golden-set under `tests/data/golden_set.jsonl` and wire the harness to the test.
- Decide gating thresholds and add CI job to run the harness on PRs.
