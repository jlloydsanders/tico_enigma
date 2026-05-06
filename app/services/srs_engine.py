from dataclasses import dataclass
import sqlite3
import numpy as np


@dataclass(frozen=True)
class SRSState:
    reps: int
    easiness_factor: float
    interval: int

    @classmethod
    def from_row(cls, row: sqlite3.Row):
        """
        Factory method to create an SRSState from a database row.
        Handles the mapping from SQL columns to class attributes.
        """
        if row is None:
            # Return a 'New Node' state if no record exists
            return cls(reps=0, easiness_factor=2.5, interval=0)

        return cls(
            reps=row["reps"],
            easiness_factor=row["easiness_factor"],
            interval=row["interval"]
        )

class SRSEngine:
    @staticmethod
    def calculate_next_review(current_state: SRSState, quality: int) -> SRSState:
        """
        Calculates the next state based on SM-2 logic.
        Quality (q) is 0-5.
        3 or higher is a 'pass'.
        """

        # At the very start of the method
        quality = int(np.clip(quality, 0, 5))

        # 1. Failure Logic (q < 3)
        if quality < 3:
            return SRSState(
                reps=0,
                easiness_factor=current_state.easiness_factor,
                interval=1
            )

        # 2. Update Easiness Factor (EF)
        # Formula: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        q_diff = 5 - quality
        ef_delta = 0.1 - (q_diff * (0.08 + (q_diff * 0.02)))

        # Enforce 1.3 floor from Project Bible using NumPy
        new_ef = float(np.maximum(1.3, current_state.easiness_factor + ef_delta))

        # 3. Calculate Interval and Update Reps
        new_reps = current_state.reps + 1

        if new_reps == 1:
            new_interval = 1
        elif new_reps == 2:
            new_interval = 6
        else:
            # Cast to int to ensure database compatibility
            new_interval = int(np.round(current_state.interval * new_ef))

        return SRSState(
            reps=new_reps,
            easiness_factor=new_ef,
            interval=new_interval
        )