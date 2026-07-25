"""Simple tracing utilities for local testing.

Provides a `timer` context manager that records elapsed milliseconds into the
metrics histogram with the provided metric name.
"""
from contextlib import contextmanager
from time import perf_counter
from . import metrics


@contextmanager
def timer(metric_name: str):
    start = perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (perf_counter() - start) * 1000.0
        try:
            metrics.record_histogram(metric_name, elapsed_ms)
        except Exception:
            # Tracing should never raise during collection in tests
            pass
