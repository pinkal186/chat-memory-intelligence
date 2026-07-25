"""Evaluation harness for golden-set retrieval regression tests.

This is a minimal harness that reads a JSONL golden set and computes per-query
precision and recall against a provided retriever function.
"""
import json
from typing import Callable, Dict


def run_golden_set(path: str, store, retriever: Callable, top_k: int = 10) -> Dict:
    """Run golden set JSONL at `path` against `retriever(store, user_id)`.

    Golden-set JSONL format: one JSON object per line with keys:
      - user_id: str
      - query: str (ignored by this prototype; included for future harnesses)
      - expected_ids: list[str]

    Returns dict with average precision and recall under keys `precision` and `recall`.
    """
    precisions = []
    recalls = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            user_id = obj.get("user_id")
            expected = obj.get("expected_ids", [])
            rows = retriever(store, user_id)
            returned_ids = [r.id for r in rows][:top_k]
            if returned_ids:
                tp = len([_ for _ in returned_ids if _ in expected])
                precision = tp / len(returned_ids)
            else:
                precision = 0.0
            recall = 0.0
            if expected:
                recall = len([_ for _ in expected if _ in returned_ids]) / len(expected)
            precisions.append(precision)
            recalls.append(recall)
    avg_p = sum(precisions) / len(precisions) if precisions else 0.0
    avg_r = sum(recalls) / len(recalls) if recalls else 0.0
    return {"precision": avg_p, "recall": avg_r, "cases": len(precisions)}
