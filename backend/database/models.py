CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    features TEXT DEFAULT '',
    problem TEXT DEFAULT '',
    audience TEXT NOT NULL,
    price_range TEXT DEFAULT '',
    competitors TEXT DEFAULT '',
    platform TEXT NOT NULL,
    tone TEXT NOT NULL,
    requirements TEXT DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_PREFERENCES_TABLE = """
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    preference TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'Positive',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id)
);
"""

CREATE_GENERATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS generations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    tone TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id)
);
"""

CREATE_FEEDBACK_TABLE = """
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generation_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    feedback TEXT NOT NULL,
    sentiment TEXT DEFAULT 'Positive',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(generation_id) REFERENCES generations(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
"""

CREATE_TREND_SNAPSHOTS_TABLE = """
CREATE TABLE IF NOT EXISTS trend_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    media_type TEXT NOT NULL,
    title TEXT NOT NULL,
    tags TEXT DEFAULT '[]',
    url TEXT DEFAULT '',
    metrics TEXT DEFAULT '{}',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TREND_ANALYSES_TABLE = """
CREATE TABLE IF NOT EXISTS trend_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    industry TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TREND_PREDICTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS trend_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    industry TEXT NOT NULL,
    prediction TEXT NOT NULL,
    confidence REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""
