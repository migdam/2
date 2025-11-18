CREATE TABLE IF NOT EXISTS strategies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    embedding BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    best_match TEXT,
    score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER,
    chunk_text TEXT NOT NULL,
    best_match TEXT,
    score REAL,
    explanation TEXT,
    embedding BLOB NOT NULL,
    FOREIGN KEY(content_id) REFERENCES content(id)
);

CREATE TABLE IF NOT EXISTS pca_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vector BLOB,
    label TEXT
);
