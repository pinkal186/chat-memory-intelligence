"""Lightweight in-memory metrics collector for local testing.

This is intentionally minimal: counters and histograms stored in process memory so
unit tests can assert that metrics would be emitted. Replace with Prometheus/OpenTelemetry
exporters in production.
"""
from typing import Dict, List

_counters: Dict[str, int] = {}
_histograms: Dict[str, List[float]] = {}


def incr(name: str, amount: int = 1):
    _counters[name] = _counters.get(name, 0) + int(amount)


def record_histogram(name: str, value: float):
    _histograms.setdefault(name, []).append(float(value))


def get_counter(name: str) -> int:
    return _counters.get(name, 0)


def get_histogram(name: str) -> List[float]:
    return _histograms.get(name, [])


def reset():
    _counters.clear()
    _histograms.clear()
