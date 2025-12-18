import streamlit as st
import numpy as np

st.title("Outfit Preference Survey (Content-Based)")

# =========================
# 1. Genre definition
# =========================
genres = [
    "Casual",
    "Street",
    "Mode",
    "Minimal",
    "Formal",
    "Outdoor"
]

# =========================
# 2. Genre similarity matrix
# =========================
# 0.0 ~ 1.0 (hand-designed, editable later)
similarity = {
    "Casual":   {"Street": 0.7, "Minimal": 0.6, "Outdoor": 0.5},
    "Street":   {"Casual": 0.7, "Mode": 0.6},
    "Mode":     {"Street": 0.6, "Formal": 0.7, "Minimal": 0.5},
    "Minimal":  {"Casual": 0.6, "Mode": 0.5, "Formal": 0.6},
    "Formal":   {"Mode": 0.7, "Minimal": 0.6},
    "Outdoor":  {"Casual": 0.5}
}

# =========================
# 3. User input (0–5 or Unknown)
# =========================
st.header("Rate your preference (0–5)")

user_scores = {}

for genre in genres:
    score = st.selectbox(
        f"{genre}",
        options=["Unknown", 0, 1, 2, 3, 4, 5],
        key=genre
    )
    user_scores[genre] = None if score == "Unknown" else score

# =========================
# 4. Content-based score completion
# =========================
def complete_scores(user_scores, similarity):
    completed = user_scores.copy()

    for genre, score in completed.items():
        if score is None:
            weighted_sum = 0
            weight_total = 0

            for g, g_score in user_scores.items():
                if g_score is not None and g in similarity.get(genre, {}):
                    w = similarity[genre][g]
                    weighted_sum += g_score * w
                    weight_total += w

            completed[genre] = round(weighted_sum / weight_total, 2) if weight_total > 0 else 0

    return completed

# =========================
# 5. Recommendation
# =========================
if st.button("Recommend Outfit"):
    completed_scores = complete_scores(user_scores, similarity)

    st.subheader("Completed Preference Scores")
    st.write(completed_scores)

    # Top 3 genres
    top_genres = sorted(
        completed_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    st.subheader("Top 3 Recommended Styles")
    for genre, score in top_genres:
        st.write(f"• {genre} (score: {score})")

    # この top_genres を
    # 👉 次ステップで outfit / image generation に接続

