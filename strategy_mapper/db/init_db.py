import sqlite3
import pickle
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.embeddings import get_embedding

DB_PATH = "strategy_mapper.db"

DEFAULT_STRATEGIES = {
    "Innovation": "Developing new AI-driven products, automation, creativity.",
    "Operational Excellence": "Improving processes, reducing waste, boosting quality.",
    "Sustainability": "Energy efficiency, carbon reduction, long-term resilience."
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path) as f:
        conn.executescript(f.read())

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM strategies")
    count = cur.fetchone()[0]

    if count == 0:
        print("Seeding default strategies...")
        for name, desc in DEFAULT_STRATEGIES.items():
            emb = get_embedding(desc)
            cur.execute(
                "INSERT INTO strategies (name, description, embedding) VALUES (?, ?, ?)",
                (name, desc, pickle.dumps(emb))
            )
        conn.commit()
        print("Done.")
    else:
        print("Strategies already initialized.")

    conn.close()

if __name__ == "__main__":
    init_db()
