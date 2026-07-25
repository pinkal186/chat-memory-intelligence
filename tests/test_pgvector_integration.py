from memory.sql_store import generate_pgvector_schema


def test_generate_pgvector_schema_contains_vector_column():
    ddl = generate_pgvector_schema()
    assert "CREATE EXTENSION" in ddl
    assert "embedding" in ddl
    assert "vector(" in ddl
import os
import sys
import pytest

# Ensure repo root is on sys.path so `src` imports resolve when running pytest here.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.memory.sql_store import PostgresMemoryStore


def test_create_table_sql_contains_embedding():
    assert "embedding" in PostgresMemoryStore.CREATE_TABLE_SQL
    assert "vector(1536)" in PostgresMemoryStore.CREATE_TABLE_SQL