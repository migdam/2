import sqlite3
import pickle

DB_PATH = "strategy_mapper.db"

def connect():
    return sqlite3.connect(DB_PATH)

def fetch_strategies():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, embedding FROM strategies")
    rows = cur.fetchall()
    conn.close()
    return [(id_, name, desc, pickle.loads(emb)) for id_, name, desc, emb in rows]

def insert_strategy(name, desc, emb):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO strategies (name, description, embedding) VALUES (?, ?, ?)",
        (name, desc, pickle.dumps(emb))
    )
    conn.commit()
    conn.close()

def delete_strategy(id_):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM strategies WHERE id=?", (id_,))
    conn.commit()
    conn.close()

def insert_content(text, best_match, score):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO content (text, best_match, score) VALUES (?, ?, ?)",
        (text, best_match, score)
    )
    content_id = cur.lastrowid
    conn.commit()
    conn.close()
    return content_id

def insert_chunk(content_id, text, best_match, score, explanation, emb):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chunks (content_id, chunk_text, best_match, score, explanation, embedding) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (content_id, text, best_match, score, explanation, pickle.dumps(emb))
    )
    conn.commit()
    conn.close()

def fetch_content():
    conn = connect()
    df = None
    try:
        import pandas as pd
        df = pd.read_sql_query("SELECT * FROM content ORDER BY created_at DESC", conn)
    finally:
        conn.close()
    return df
