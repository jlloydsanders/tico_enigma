import sqlite3

# Default production path
DB_PATH = "tico_enigma.db"

def get_db_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Creates and returns a connection to the SQLite database."""
    # CRITICAL FIX: Use the db_path argument, not the global DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the production database."""
    conn = get_db_connection(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            node_id TEXT PRIMARY KEY,
            reps INTEGER DEFAULT 0,
            easiness_factor REAL DEFAULT 2.5,
            interval INTEGER DEFAULT 0,
            next_review DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_PATH}")

if __name__ == "__main__":
    init_db()