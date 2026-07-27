# Postgres + pgvector integration

Summary
-------
This note summarizes practical steps and trade-offs for using PostgreSQL with the `pgvector`
extension to store and query embedding vectors for the long-term memory tier (production
persistence for chat-memory-intelligence).

Key points
----------
- Use PostgreSQL + `pgvector` as the long-term vector store when you want a single relational
  datastore with ACID guarantees and simple operational model.
- Store embeddings as a `vector` column (dimension `d` must match your embedding model).
- Create an index on the `vector` column (IVF or HNSW where supported) to accelerate
  nearest-neighbour queries. Tune index parameters (`lists`, `ef_search`, etc.) based on
  dataset size and latency/throughput targets.
- Keep a separate typed schema fields for provenance and metadata (e.g., `user_id`,
  `source`, `importance`, `confidence`, `created_at`) so retrieval can blend semantic
  score with recency/importance/frequency signals.
- Consider hybrid search: first filter by metadata (tenant `user_id`, recency window), then
  run a vector nearest-neighbours query on the reduced candidate set to respect tenant
  isolation and improve performance.
- For heavy write throughput or very large corpora, consider specialized vector DBs
  (Milvus, Weaviate, Pinecone) or a sharded Postgres topology — but `pgvector` is a good
  default for MVP and modest scale.

Recommended implementation notes
--------------------------------
- Install and enable the `pgvector` extension in Postgres (DB admin step).
- Schema example (SQL):

```sql
CREATE TABLE memories (
  id UUID PRIMARY KEY,
  user_id TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding vector(1536), -- match embedding dim
  importance REAL DEFAULT 0,
  confidence REAL DEFAULT 0,
  source TEXT,
  created_at timestamptz DEFAULT now()
);
-- create an index (example with ivfflat):
CREATE INDEX ON memories USING ivfflat (embedding) WITH (lists = 100);
```

- Python clients: use `psycopg[binary]` or `asyncpg` + the `pgvector` Python helper (or send
  embeddings as raw arrays). Keep the embedding dimension enforced at insert time.
- Query pattern: filter by `user_id` and optional metadata; compute semantic distance with
  `embedding <-> query_embedding` (distance) and combine with other signals in application
  code or in SQL scoring expressions.

Operational tips
----------------
- Monitor index maintenance: ivf indexes need to be trained/maintained; benchmark `lists`
  and keep an eye on VACUUM/ANALYZE for large write workloads.
- Measure p95 retrieval latency; if it exceeds SLOs, tune index or move to specialized
  vector store.
- Securely restrict access to the Postgres instance and enforce row-level tenant scoping by
  indexing `user_id` and using query-time filters (and/or Postgres RLS policies for hard
  enforcement).

Alternatives
------------
- Milvus / Weaviate / Pinecone: specialized vector stores with managed scaling and advanced
  ANN algorithms. Consider when dataset size or throughput outgrows a single Postgres.
- SQLite + FAISS (local dev): useful for test environments but not production multi-tenant.

References
----------
- pgvector docs (extension + usage) — install + SQL examples
- Consider vendor docs for HNSW/IVF tuning when scaling indexes
