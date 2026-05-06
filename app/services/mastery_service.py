from app.services.srs_engine import SRSState, SRSEngine
from app.database import get_db_connection
from datetime import datetime, timedelta


class MasteryService:
    def __init__(self, db_path: str = "tico_enigma.db"):
        self.db_path = db_path
        
    def update_node_mastery(self, node_id: str, quality: int) -> SRSState:
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # 1. Fetch current state
        query = "SELECT reps, easiness_factor, interval FROM user_progress WHERE node_id = ?"
        row = cursor.execute(query, (node_id,)).fetchone()

        # 2. Convert to Object (handles new words automatically via from_row)
        current_state = SRSState.from_row(row)

        # 3. Calculate next state
        new_state = SRSEngine.calculate_next_review(current_state, quality)

        # 4. Persistence (The Save Step)
        # Calculate next_review date: Now + Interval (days)
        next_date = (datetime.now() + timedelta(days=new_state.interval)).isoformat()

        save_query = """
            INSERT INTO user_progress (node_id, reps, easiness_factor, interval, next_review)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(node_id) DO UPDATE SET
                reps=excluded.reps,
                easiness_factor=excluded.easiness_factor,
                interval=excluded.interval,
                next_review=excluded.next_review
        """

        cursor.execute(save_query, (
            node_id,
            new_state.reps,
            new_state.easiness_factor,
            new_state.interval,
            next_date
        ))

        conn.commit()
        conn.close()

        return new_state

    def get_due_nodes(self, current_time: str, limit: int = 10) -> list[str]:
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # 1. Fetch current state
        query = "SELECT node_id FROM user_progress WHERE next_review <= ? ORDER BY next_review"
        review_list = cursor.execute(query, (current_time,)).fetchall()

        # Query using the limit parameter
        query = "SELECT node_id FROM user_progress WHERE next_review <= ? ORDER BY next_review LIMIT ?"
        rows = cursor.execute(query, (current_time, limit)).fetchall()

        # Extract the string IDs from the Row objects using List Comprehension
        review_list = [row["node_id"] for row in rows]

        conn.close()

        return review_list