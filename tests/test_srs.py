import os
from datetime import datetime, timedelta

import pytest
from app.services.mastery_service import MasteryService
import sqlite3
from app.database import init_db, get_db_connection

# A temporary DB for testing
TEST_DB = "test_tico.db"


@pytest.fixture()
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
    conn.commit()
    conn.close()

    yield MasteryService(db_path=TEST_DB)

    os.remove(TEST_DB)


def test_new_word_insertion(service):
    # Arrange
    node_id = "tuanis"
    quality = 5

    # Act
    state = service.update_node_mastery(node_id, quality)

    # Assert
    assert state.reps == 1
    assert state.interval == 1

    # Verify the database actually saved it
    conn = sqlite3.connect(TEST_DB)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM user_progress WHERE node_id = ?", (node_id,)).fetchone()
    conn.close()

    assert row is not None
    assert row["reps"] == 1
    assert row["interval"] == 1


def test_interval_jump(service):
    # Arrange
    node_id = "mae"
    quality = 5

    # Act - First review (reps 0 -> 1)
    service.update_node_mastery(node_id, quality)

    # Act - Second review (reps 1 -> 2)
    state = service.update_node_mastery(node_id, quality)

    # Assert
    assert state.reps == 2
    assert state.interval == 6

def test_failure_reset(service):
    # Arrange - Build the word up to reps=2 first
    node_id = "pura_vida"
    service.update_node_mastery(node_id, 5)
    service.update_node_mastery(node_id, 5)

    # Act - The user forgets the word (quality = 2)
    state = service.update_node_mastery(node_id, 2)

    # Assert
    assert state.reps == 0
    assert state.interval == 1
    # The Easiness Factor drops, but reps/interval are the critical resets

def test_ease_hell_floor(service):
    # Arrange - Inject a word that is right on the edge of the floor (EF = 1.4)
    node_id = "murciélago"
    conn = sqlite3.connect(service.db_path)
    conn.execute(
        "INSERT INTO user_progress (node_id, reps, easiness_factor, interval) VALUES (?, ?, ?, ?)",
        (node_id, 3, 1.4, 10)
    )
    conn.commit()
    conn.close()

    # Act - A score of 3 normally reduces EF by 0.14.
    # 1.4 - 0.14 = 1.26. The floor should catch it and set it to 1.3.
    state = service.update_node_mastery(node_id, 3)

    # Assert
    assert state.easiness_factor == 1.3

def test_retrieve_empty_word_list(service):
    # Pass current time as an ISO string
    now_str = datetime.now().isoformat()
    wordlist = service.get_due_nodes(current_time=now_str)

    assert len(wordlist) == 0

def test_retrieve_non_empty_word_list(service):
    service.update_node_mastery("tuanis", 1)
    service.update_node_mastery("mapa", 1)
    service.update_node_mastery("hola", 1)

    # Act - Fast forward time by 2 days so the words become "overdue"
    future_time = (datetime.now() + timedelta(days=2)).isoformat()
    wordlist = service.get_due_nodes(current_time=future_time)

    assert len(wordlist) == 3