import os
import sqlite3
import pytest
from app.services.mastery_service import MasteryService

TEST_DB = os.path.abspath("test_tico_enigma.db")

@pytest.fixture
def service():
    """Create a fresh database before every test and delete it after."""
    # This is a 'Principal' pattern: clean slate for every test
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    # We need a way to tell init_db which file to use
    # For now, let's just manually init it for the test

    conn = sqlite3.connect(TEST_DB)
    conn.execute("""
            CREATE TABLE user_progress (
                node_id TEXT PRIMARY KEY,
                reps INTEGER,
                easiness_factor REAL,
                interval INTEGER,
                next_review DATETIME
            )
        """)

    conn.execute("""
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

    yield MasteryService(db_path=TEST_DB)

    os.remove(TEST_DB)