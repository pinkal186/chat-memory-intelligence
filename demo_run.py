import os
import sys

ROOT = os.path.abspath(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.extractor import extract_memories
from memory.evaluator import evaluate_candidate
from memory.store import MemoryStore

def main():
    store = MemoryStore()
    turn = "I'm building a product that uses Postgres and pgvector."
    for c in extract_memories(turn, user_id="u1"):
        keep = evaluate_candidate(c)
        print(f"candidate: {c.content!r} -> keep={keep}")
        if keep:
            store.add(c)
    print("stored:", [r.content for r in store.query_by_user("u1")])

if __name__ == '__main__':
    main()
