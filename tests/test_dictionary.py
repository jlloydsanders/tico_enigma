import sqlite3

from app.services.dictionary_engine import DictionaryEntry


def test_new_dictionary_entry_insertion(service):
    # Arrange
    node_id = "banco_finance"
    spanish = "banco"
    english = "bank"
    exaple_sentences = "banco banco banco banco banco"

    # Act
    dictionary_entry = DictionaryEntry(node_id, spanish, english, exaple_sentences)

    # Assert
    assert dictionary_entry.node_id == node_id
    assert dictionary_entry.spanish == spanish
    assert dictionary_entry.english == english
    assert dictionary_entry.example_sentences == exaple_sentences

    service.save_dictionary_entry(dictionary_entry)

    # Verify the database actually saved it
    conn = sqlite3.connect(service.db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM dictionary WHERE node_id = ?", (node_id,)).fetchone()
    conn.close()

    assert row is not None
    assert row["node_id"] == node_id
    assert row["spanish"] == spanish
    assert row["english"] == english
    assert row["example_sentences"] == exaple_sentences

def test_retrieve_dictionary_entry(service):
    dictionary_entry = DictionaryEntry("banco_finance", "banco", "bank", "banco banco banco banco")
    service.save_dictionary_entry(dictionary_entry)

    retrieved_dictionary_entry = service.get_dictionary_entry("banco_finance")

    # Assert
    assert retrieved_dictionary_entry.node_id == "banco_finance"
    assert retrieved_dictionary_entry.spanish == "banco"
    assert retrieved_dictionary_entry.english == "bank"
    assert retrieved_dictionary_entry.example_sentences == "banco banco banco banco"
