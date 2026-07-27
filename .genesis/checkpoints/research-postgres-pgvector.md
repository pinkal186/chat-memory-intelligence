## L3 Research · 2026-07-25
- topic: Postgres + pgvector integration for production persistence
- wiki page written: [.genesis/wiki/concepts/Postgres-pgvector-integration.md](.genesis/wiki/concepts/Postgres-pgvector-integration.md)
- sources checked: pgvector docs (local), Postgres indexing references, vector DB comparisons (Milvus/Weaviate)

Findings summary:
- `pgvector` is a suitable MVP choice: keeps architecture simple and provides ACID guarantees.
- Ensure embedding dimension is fixed and enforced at insert time; create an ANN index (ivfflat
  / hnsw where available) for low-latency search.
- Hybrid search (metadata filter → vector NN) enforces tenant isolation and helps performance.
- For large-scale or high-throughput use cases, evaluate a specialized vector DB as an exit
  strategy.

Next recommended actions:
1. Prototype `pgvector` schema and index locally using a test Postgres instance.
2. Add integration tests that exercise multi-tenant filtering + vector retrieval (to guard M3
   invariant: no cross-user leakage).
3. If prototyping shows latency issues, research migrating embeddings to a dedicated vector DB.
