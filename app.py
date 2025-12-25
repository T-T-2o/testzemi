import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(layout="wide")
st.title("Content-Based Outfit Recommendation")

# =====================
# 1. Master Data
# =====================

GENRES = ["Streetwear", "Casual", "Minimal", "Mode", "Outdoor"]

GENRE_ITEMS = {
    "Streetwear": ["Graphic Tee", "Hoodie", "Wide Pants", "Sneakers", "Coach Jacket"],
    "Casual": ["Sweatshirt", "Denim Jacket", "Chinos", "Sneakers"],
    "Minimal": ["Plain Shirt", "Slacks", "Loafers", "Simple Jacket"],
    "Mode": ["Tailored Jacket", "Black Pants", "Boots"],
    "Outdoor": ["Shell Jacket", "Fleece", "Cargo Pants", "Hiking Shoes"]
}

COLORS = {
    "Black": (40, 40, 40),
    "Navy": (50, 70, 110),
    "Beige": (210, 200, 170),
    "Green": (70, 120, 90),
    "Gray": (140, 140, 140),
    "Red": (150, 70, 70)
}

# =====================
# 2. User Input
# =====================

st.header("Your Preferences")

gender = st.selectbox("Gender", ["Male", "Female"])

st.subheader("Genre Preference (0–5, blank = unknown)")
genre_score_input = {}
for g in GENRES:
    genre_score_input[g] = st.slider(g, 0, 5, 0)

st.subheader("Color Preference (0–5, blank = unknown)")
color_score_input = {}
for c in COLORS.keys():
    color_score_input[c] = st.slider(c, 0, 5, 0)

# =====================
# 3. Content-Based Scoring
# =====================

def normalize_scores(scores: dict):
    known = [v for v in scores.values() if v > 0]
    avg = sum(known) / len(known) if known else 2.5
    return {k: (v if v > 0 else avg) for k, v in scores.items()}

genre_scores = normalize_scores(genre_score_input)
color_scores = normalize_scores(color_score_input)

top_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)[:3]
top_colors = sorted(color_scores.items(), key=lambda x: x[1], reverse=True)

# =====================
# 4. Outfit Generator
# =====================

def generate_outfit(genre):
    items = random.sample(GENRE_ITEMS[genre], k=min(3, len(GENRE_ITEMS[genre])))
    color_candidates = [c for c, _ in top_colors[:3]]
    color = random.choice(color_candidates)
    return items, color

# =====================
# 5. Image Generator
# =====================

from PIL import Image, ImageDraw

def generate_image(color_rgb, gender):
    img = Image.new("RGB", (260, 460), "white")
    d = ImageDraw.Draw(img)

    skin = (220, 200, 180)
    outline = "black"

    # =====================
    # Head (common)
    # =====================
    d.ellipse((110, 20, 150, 60), fill=skin, outline=outline)

    if gender == "Male":
        # =====================
        # Male (toilet sign style)
        # =====================

        # Torso
        d.rectangle(
            (100, 70, 160, 180),
            fill=color_rgb,
            outline=outline
        )

        # Arms
        d.rectangle((80, 80, 100, 180), fill=color_rgb, outline=outline)
        d.rectangle((160, 80, 180, 180), fill=color_rgb, outline=outline)

        # Legs
        d.rectangle((105, 180, 125, 360), fill=color_rgb, outline=outline)
        d.rectangle((135, 180, 155, 360), fill=color_rgb, outline=outline)

    else:
        # =====================
        # Female (toilet sign style)
        # =====================

        # Upper torso
        d.rectangle(
            (110, 70, 150, 150),
            fill=color_rgb,
            outline=outline
        )

        # Arms
        d.rectangle((90, 80, 110, 160), fill=color_rgb, outline=outline)
        d.rectangle((150, 80, 170, 160), fill=color_rgb, outline=outline)

        # Skirt (triangle)
        d.polygon(
            [
                (130, 150),   # top
                (70, 320),    # left bottom
                (190, 320)    # right bottom
            ],
            fill=color_rgb,
            outline=outline
        )

        # Legs (short)
        d.rectangle((115, 320, 130, 400), fill=color_rgb, outline=outline)
        d.rectangle((130, 320, 145, 400), fill=color_rgb, outline=outline)

    return img



# =====================
# 6. Output
# =====================

st.header("Recommended Outfits (Top 3 Genres)")

cols = st.columns(3)

for idx, (genre, score) in enumerate(top_genres):
    with cols[idx]:
        items, color_name = generate_outfit(genre)
        color_rgb = COLORS[color_name]

        st.subheader(f"{genre}")
        st.write("**Items:**", ", ".join(items))
        st.write("**Color:**", color_name)

        img = generate_image(color_rgb, gender)
        st.image(img)

# =====================
# 7. Score Display
# =====================

st.header("Content-Based Recommendation Scores")

st.subheader("Genre Scores")
st.json(genre_scores)

st.subheader("Color Scores")
st.json(color_scores)
