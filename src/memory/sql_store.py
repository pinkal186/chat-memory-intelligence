from typing import List, Optional
from .schema import MemoryRecord
import logging
from . import audit_log

try:
    from sqlalchemy import create_engine, text
    SQLALCHEMY_AVAILABLE = True
except Exception:
    SQLALCHEMY_AVAILABLE = False


def generate_pgvector_schema(table_name: str = "memories") -> str:
    """Return a SQL DDL snippet that creates a Postgres table suitable for pgvector.

    This function is safe to call in environments without SQLAlchemy or Postgres; it
    only returns the SQL string so tests can assert the intended schema shape.
    """
    return f"""
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS {table_name} (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    type TEXT,
    content TEXT,
    importance DOUBLE PRECISION,
    confidence DOUBLE PRECISION,
    source TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    embedding vector(1536)
);
"""


class SQLMemoryStore:
    """A lightweight prototype wrapper for a Postgres + pgvector memory store.

    In this prototype the code prefers to only generate schema and DDL when SQLAlchemy or
    a Postgres server is not available. Full read/write operations are left as explicit
    TODOs to be completed during an integration pass (M3 integration).
    """

    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url
        if SQLALCHEMY_AVAILABLE and db_url:
            self.engine = create_engine(db_url)
        else:
            self.engine = None

    def create_tables(self, table_name: str = "memories") -> Optional[str]:
        """Create tables in the database if possible, otherwise return the DDL string.

        Returns the DDL string when no DB driver is available so callers can inspect
        or apply it manually.
        """
        ddl = generate_pgvector_schema(table_name)
        if self.engine is None:
            logging.info("SQL engine not configured; returning DDL string only")
            return ddl
        # Prefer executing raw SQL to keep prototype dependencies minimal
        with self.engine.begin() as conn:
            conn.execute(text(ddl))
        return None

    def add(self, record: MemoryRecord, embedding: Optional[List[float]] = None):
        if self.engine is None:
            raise RuntimeError("SQL engine not available in this environment")
        # Full implementation omitted in prototype — DB insert logic goes here.
        raise NotImplementedError("Add operation not implemented in prototype")

    def query_by_user(self, user_id: str) -> List[MemoryRecord]:
        if self.engine is None:
            raise RuntimeError("SQL engine not available in this environment")
        # Full implementation omitted in prototype — DB select logic goes here.
        raise NotImplementedError("Query operation not implemented in prototype")
import sqlite3
from typing import List
from .schema import MemoryRecord
from datetime import datetime
from typing import Optional


try:
    import psycopg
except Exception:
    psycopg = None


class SQLiteMemoryStore:
    """Simple SQLite-backed store for local development/testing."""

    def __init__(self, path: str = ":memory:"):
        self.path = path
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self._ensure_table()

    def _ensure_table(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                type TEXT,
                content TEXT,
                importance REAL,
                confidence REAL,
                source TEXT,
                created_at TEXT
            )
            """
        )
        # audit_log table for governance (append-only)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                memory_id TEXT,
                user_id TEXT,
                details TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        self.conn.commit()

    def add(self, record: MemoryRecord):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO memories (id,user_id,type,content,importance,confidence,source,created_at) VALUES (?,?,?,?,?,?,?,?)",
            (
                record.id,
                record.user_id,
                record.type,
                record.content,
                record.importance,
                record.confidence,
                record.source,
                record.created_at.isoformat(),
            ),
        )
        self.conn.commit()
        # write audit row for persistence
        try:
            cur.execute(
                "INSERT INTO audit_log (event_type,memory_id,user_id,details) VALUES (?,?,?,?)",
                ("write", record.id, record.user_id, record.source),
            )
            self.conn.commit()
        except Exception:
            # best effort
            pass
        try:
            audit_log.record("write", memory_id=record.id, user_id=record.user_id, details={"source": record.source})
        except Exception:
            pass

    def query_by_user(self, user_id: str) -> List[MemoryRecord]:
        cur = self.conn.cursor()
        cur.execute("SELECT id,user_id,type,content,importance,confidence,source,created_at FROM memories WHERE user_id = ?", (user_id,))
        rows = cur.fetchall()
        out: List[MemoryRecord] = []
        for r in rows:
            rec = MemoryRecord(
                id=r[0],
                user_id=r[1],
                type=r[2],
                content=r[3],
                importance=float(r[4] or 0.0),
                confidence=float(r[5] or 0.0),
                source=r[6] or "",
                created_at=datetime.fromisoformat(r[7]) if r[7] else datetime.utcnow(),
            )
            out.append(rec)
        return out

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass

    def delete_by_id(self, memory_id: str):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        self.conn.commit()
        try:
            cur.execute("INSERT INTO audit_log (event_type,memory_id) VALUES (?,?)", ("delete", memory_id))
            self.conn.commit()
        except Exception:
            pass
        try:
            audit_log.record("delete", memory_id=memory_id)
        except Exception:
            pass


class PostgresMemoryStore:
    """Prototype Postgres-backed store that includes a `pgvector` embedding column.

    This class is a light prototype: it exposes the table creation SQL in
    `CREATE_TABLE_SQL` so unit tests can validate the schema without a live DB.
    If `psycopg` is available, the `ensure_table()` method will attempt to run
    the SQL against the provided connection.
    """

    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS memories (
      id UUID PRIMARY KEY,
      user_id TEXT NOT NULL,
      type TEXT,
      content TEXT,
      importance REAL DEFAULT 0,
      confidence REAL DEFAULT 0,
      source TEXT,
      created_at timestamptz DEFAULT now(),
      embedding vector(1536)
    );
    -- example index: CREATE INDEX ON memories USING ivfflat (embedding) WITH (lists = 100);
    """

    def __init__(self, dsn: str):
        if not psycopg:
            raise RuntimeError("psycopg not installed; PostgresMemoryStore requires psycopg")
        self.dsn = dsn
        self.conn = psycopg.connect(dsn)

    def ensure_table(self):
        with self.conn.cursor() as cur:
            cur.execute(self.CREATE_TABLE_SQL)
        self.conn.commit()

    def add(self, record: MemoryRecord, embedding: Optional[List[float]] = None):
        with self.conn.cursor() as cur:
            sql = (
                "INSERT INTO memories (id,user_id,type,content,importance,confidence,source,created_at,embedding) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            )
            cur.execute(
                sql,
                (
                    record.id,
                    record.user_id,
                    record.type,
                    record.content,
                    record.importance,
                    record.confidence,
                    record.source,
                    record.created_at,
                    embedding,
                ),
            )
        self.conn.commit()

    def query_by_user(self, user_id: str) -> List[MemoryRecord]:
        out: List[MemoryRecord] = []
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id,user_id,type,content,importance,confidence,source,created_at FROM memories WHERE user_id = %s",
                (user_id,),
            )
            rows = cur.fetchall()
            for r in rows:
                rec = MemoryRecord(
                    id=str(r[0]),
                    user_id=r[1],
                    type=r[2],
                    content=r[3],
                    importance=float(r[4] or 0.0),
                    confidence=float(r[5] or 0.0),
                    source=r[6] or "",
                    created_at=r[7] if isinstance(r[7], datetime) else datetime.fromisoformat(r[7]),
                )
                out.append(rec)
        return out

    def delete_by_id(self, memory_id: str):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM memories WHERE id = %s", (memory_id,))
        self.conn.commit()

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass
