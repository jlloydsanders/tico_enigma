import sqlite3
from pathlib import Path

# 1. Anchor to the script's actual location on the hard drive.
# __file__ is the path to this specific python file.
# Assuming this is in /app/database.py:
# .parent = /app
# .parent.parent = The project root folder
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# 2. Define the data directory relative to the project root
DATA_DIR = PROJECT_ROOT / "data"

# 3. CRITICAL: Create the directory if it doesn't exist.
# SQLite will crash if you try to make a file inside a non-existent folder.
DATA_DIR.mkdir(exist_ok=True)

# 4. Define the final, absolute path to the database
DB_PATH = DATA_DIR / "memory_engine.db"

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

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS dictionary (
                node_id TEXT PRIMARY KEY,
                spanish TEXT NOT NULL,
                english TEXT NOT NULL,
                example_sentences TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_PATH}")

if __name__ == "__main__":
    init_db()