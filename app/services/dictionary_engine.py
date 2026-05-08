import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class DictionaryEntry:
    node_id: str
    spanish: str
    english: str
    example_sentences: str

    @classmethod
    def from_row(cls, row: sqlite3.Row):
        """
        Factory method to create an SRSState from a database row.
        Handles the mapping from SQL columns to class attributes.
        """
        if row is None:
            # Return a 'New Node' state if no record exists
            return cls(node_id="", spanish="", english="", example_sentences="")

        return cls(
            node_id=row["node_id"],
            spanish=row["spanish"],
            english=row["english"],
            example_sentences=row["example_sentences"]
        )