"""Comprehensive demo showing the full memory system flow."""
import os
import sys

ROOT = os.path.abspath(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.extractor import extract_memories
from memory.evaluator import evaluate_candidate
from memory.store import MemoryStore
from memory.retriever import retrieve_for_user
from memory.corrections import apply_correction
from memory.forget import forget_by_content
from memory.reflection import consolidate_scattered_facts

def main():
    print("=== Memory System Demo ===\n")
    
    store = MemoryStore()
    
    # 1. Extract and store memories
    print("1. Extracting memories from conversation turns:")
    turns = [
        "I'm building SecondBrainLabs and I use PostgreSQL.",
        "I also work with pgvector for embeddings.",
        "I deploy my apps with Docker."
    ]
    
    for turn in turns:
        print(f"   Turn: {turn!r}")
        for c in extract_memories(turn, user_id="u1"):
            keep = evaluate_candidate(c)
            if keep:
                store.add(c)
                print(f"   ✓ Stored: {c.content!r} (importance={c.importance:.2f}, confidence={c.confidence:.2f})")
    
    # 2. Retrieve memories
    print("\n2. Retrieving memories for user 'u1':")
    memories = retrieve_for_user(store, "u1")
    for i, m in enumerate(memories, 1):
        print(f"   {i}. {m.content!r}")
    
    # 3. Apply a correction
    print("\n3. Correcting a memory:")
    if memories:
        mid = memories[0].id
        print(f"   Original: {memories[0].content!r}")
        apply_correction(store, mid, new_content="I'm building SecondBrainAI with PostgreSQL", new_confidence=0.95)
        updated = retrieve_for_user(store, "u1")
        print(f"   Updated:  {updated[0].content!r} (confidence={updated[0].confidence:.2f})")
    
    # 4. Forget a memory
    print("\n4. Forgetting memories containing 'Docker':")
    deleted = forget_by_content(store, "u1", "Docker")
    print(f"   Deleted {deleted} memory(ies)")
    remaining = retrieve_for_user(store, "u1")
    print(f"   Remaining: {[m.content for m in remaining]}")
    
    # 5. Reflection (consolidate scattered facts)
    print("\n5. Consolidating scattered memories:")
    summary = consolidate_scattered_facts(store, "u1")
    if summary:
        print(f"   Summary: {summary.content!r}")
        print(f"   Count after consolidation: {len(retrieve_for_user(store, 'u1'))}")
    
    print("\n=== Demo Complete ===")

if __name__ == '__main__':
    main()
