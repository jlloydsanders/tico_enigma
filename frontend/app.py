import streamlit as st
import requests

# The URL where your FastAPI server is running
API_BASE_URL = "http://127.0.0.1:8000"

# --- UI Setup ---
st.set_page_config(page_title="Tico Enigma", page_icon="🇨🇷", layout="centered")
st.title("Tico Enigma 🧠")
st.markdown("Your AI-powered Costa Rican Spanish tutor.")

# --- State Management ---
# Streamlit reruns the script from top to bottom on every interaction.
# We use session_state to remember things between button clicks.
if "current_batch" not in st.session_state:
    st.session_state.current_batch = []
if "current_card_index" not in st.session_state:
    st.session_state.current_card_index = 0

# --- Fetch Data ---
if st.button("Start Daily Review"):
    with st.spinner("Consulting the brain..."):
        try:
            response = requests.get(f"{API_BASE_URL}/daily-review")
            response.raise_for_status()  # Check for errors

            data = response.json()
            st.session_state.current_batch = data.get("due_cards", [])
            st.session_state.current_card_index = 0

            if not st.session_state.current_batch:
                st.success("You are all caught up for today! Pura vida!")
        except Exception as e:
            st.error(f"Failed to connect to the backend: {e}")

# --- Display the Flashcard ---
if st.session_state.current_batch:
    cards = st.session_state.current_batch
    index = st.session_state.current_card_index

    # Check if we finished the batch
    if index >= len(cards):
        st.success("Review session complete! Great job.")
        if st.button("Clear Session"):
            st.session_state.current_batch = []
            st.rerun()
    else:
        current_card = cards[index]

        # The Flashcard UI
        st.divider()
        st.subheader("Translate this word:")
        st.header(current_card["node_id"].capitalize())

        # We use an expander to hide the answer until the user is ready
        with st.expander("Show Answer"):
            st.write(f"**English:** {current_card['english']}")
            st.write(f"**Spanish Context:** {current_card['spanish']}")
            st.info(f"Context: {current_card['example_sentences']}")

            st.divider()
            st.write("How well did you know this?")

            # The Grading Buttons
            col1, col2, col3, col4 = st.columns(4)
            grades = {0: "Forgot (0)", 1: "Hard (1)", 2: "Good (2)", 3: "Easy (3)"}

            for grade, label in grades.items():
                # We use the column objects to put buttons side-by-side
                button_col = [col1, col2, col3, col4][grade]
                if button_col.button(label, key=f"grade_{grade}_{current_card['node_id']}"):
                    # 1. Send the grade to the backend POST route
                    requests.post(
                        f"{API_BASE_URL}/submit-review",
                        json={"node_id": current_card["node_id"], "grade": grade}
                    )

                    # 2. Move to the next card and refresh the UI
                    st.session_state.current_card_index += 1
                    st.rerun()