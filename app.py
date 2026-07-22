
import streamlit as st
import random

st.set_page_config(page_title="Mini Pac-Man", layout="centered")

st.title("🟡 Mini Pac-Man")

SIZE = 10

if "player" not in st.session_state:
    st.session_state.player = [0, 0]
    st.session_state.food = [random.randint(0, SIZE-1), random.randint(0, SIZE-1)]
    st.session_state.score = 0

player = st.session_state.player
food = st.session_state.food

st.write(f"### Score: {st.session_state.score}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("⬆️"):
        player[0] = max(0, player[0]-1)

with col2:
    if st.button("⬇️"):
        player[0] = min(SIZE-1, player[0]+1)

with col3:
    if st.button("⬅️"):
        player[1] = max(0, player[1]-1)

with col4:
    if st.button("➡️"):
        player[1] = min(SIZE-1, player[1]+1)

if player == food:
    st.session_state.score += 1
    st.session_state.food = [
        random.randint(0, SIZE-1),
        random.randint(0, SIZE-1),
    ]
    food = st.session_state.food
    st.success("Yum! Pellet eaten!")

board = ""

for r in range(SIZE):
    for c in range(SIZE):
        if [r, c] == player:
            board += "🟡"
        elif [r, c] == food:
            board += "🔵"
        else:
            board += "⬛"
    board += "\n"

st.text(board)

if st.button("Restart"):
    st.session_state.player = [0, 0]
    st.session_state.food = [random.randint(0, SIZE-1), random.randint(0, SIZE-1)]
    st.session_state.score = 0
    st.rerun()
           
