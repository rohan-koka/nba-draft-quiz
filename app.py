import streamlit as st
import random

st.set_page_config(page_title="NBA 2025 Draft Quiz", layout="centered")

players = [
    {"name": "Cooper Flagg", "pick": 1, "team": "Dallas Mavericks"},
    {"name": "Dylan Harper", "pick": 2, "team": "San Antonio Spurs"},
    {"name": "VJ Edgecombe", "pick": 3, "team": "Philadelphia 76ers"},
    {"name": "Kon Knueppel", "pick": 4, "team": "Charlotte Hornets"},
    {"name": "Ace Bailey", "pick": 5, "team": "Utah Jazz"},
    {"name": "Tre Johnson", "pick": 6, "team": "Washington Wizards"},
    {"name": "Jeremiah Fears", "pick": 7, "team": "New Orleans Pelicans"},
    {"name": "Egor Demin", "pick": 8, "team": "Brooklyn Nets"},
    {"name": "Collin Murray-Boyles", "pick": 9, "team": "Toronto Raptors"},
    {"name": "Khaman Maluach", "pick": 10, "team": "Houston Rockets"},
    {"name": "Cedric Coward", "pick": 11, "team": "Portland Trail Blazers"},
    {"name": "Noa Essengue", "pick": 12, "team": "Chicago Bulls"},
    {"name": "Derik Queen", "pick": 13, "team": "Atlanta Hawks"},
    {"name": "Carter Bryant", "pick": 14, "team": "San Antonio Spurs"},
    {"name": "Thomas Sorber", "pick": 15, "team": "Oklahoma City Thunder"},
]

if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.used = []
    st.session_state.game_over = False
    st.session_state.show_answer = False
    st.session_state.message = ""
    st.session_state.points_earned = None
    st.session_state.current = random.choice(players)
    st.session_state.used.append(st.session_state.current)

def get_new_player():
    available = [p for p in players if p not in st.session_state.used]
    if not available:
        st.session_state.used = []
        available = players[:]
    player = random.choice(available)
    st.session_state.used.append(player)
    st.session_state.current = player

def check_guess(guess):
    actual = st.session_state.current["pick"]
    diff = abs(guess - actual)
    if diff == 0:
        points, msg = 10, f"Perfect! {st.session_state.current['name']} was pick #{actual}."
    elif diff <= 2:
        points, msg = 7, f"Close! {st.session_state.current['name']} was pick #{actual}."
    elif diff <= 5:
        points, msg = 4, f"Not bad. {st.session_state.current['name']} was pick #{actual}."
    else:
        points, msg = 0, f"Too far off. {st.session_state.current['name']} was pick #{actual}."
    st.session_state.score += points
    st.session_state.points_earned = points
    st.session_state.message = msg
    st.session_state.show_answer = True

def next_round():
    if st.session_state.round >= 10:
        st.session_state.game_over = True
        return
    st.session_state.round += 1
    st.session_state.show_answer = False
    st.session_state.message = ""
    st.session_state.points_earned = None
    get_new_player()

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.title("🏀 NBA 2025 Draft Quiz")

col1, col2 = st.columns(2)
col1.metric("Round", f"{st.session_state.round}/10")
col2.metric("Score", st.session_state.score)

st.divider()

if st.session_state.game_over:
    st.markdown("## 🏆 Game Over!")
    st.markdown(f"### Final Score: {st.session_state.score} / 100")
    if st.session_state.score >= 80:
        st.success("Elite draft knowledge!")
    elif st.session_state.score >= 50:
        st.info("Solid effort!")
    else:
        st.warning("Study up on the 2025 draft!")
    if st.button("🔄 Play Again"):
        reset_game()
else:
    player = st.session_state.current
    with st.container(border=True):
        st.markdown(f"## {player['name']}")
        st.markdown(f"**Team:** {player['team']}")
        st.markdown("**What pick was this player in the 2025 NBA Draft?**")

    if not st.session_state.show_answer:
        with st.form("guess_form"):
            guess = st.number_input("Enter pick number (1-15):", min_value=1, max_value=15, step=1)
            st.caption("⚠️ Click 'Submit Guess' — do not press Enter")
            submitted = st.form_submit_button("Submit Guess")
            if submitted:
                check_guess(guess)
                st.rerun()
    else:
        st.markdown(f"### {st.session_state.message}")
        if st.session_state.points_earned == 10:
            st.success(f"+{st.session_state.points_earned} points 🔥")
        elif st.session_state.points_earned >= 4:
            st.info(f"+{st.session_state.points_earned} points")
        else:
            st.error("+0 points")

        if st.button("Next Round ➡️"):
            next_round()
            st.rerun()