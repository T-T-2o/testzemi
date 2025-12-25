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
    "Streetwear": {
        "inner": ["Graphic Tee", "Plain Tee"],
        "outer": ["Coach Jacket", "Zip Hoodie"],
        "bottom": ["Wide Pants", "Cargo Pants"]
    },
    "Casual": {
        "inner": ["T-shirt", "Shirt"],
        "outer": ["Denim Jacket", "Cardigan"],
        "bottom": ["Chinos", "Straight Pants"]
    },
    "Minimal": {
        "inner": ["Plain Shirt"],
        "outer": ["Simple Jacket"],
        "bottom": ["Slacks"]
    },
    "Mode": {
        "inner": ["Black Shirt"],
        "outer": ["Tailored Jacket"],
        "bottom": ["Slim Pants"]
    },
    "Outdoor": {
        "inner": ["Base Layer"],
        "outer": ["Shell Jacket", "Fleece"],
        "bottom": ["Cargo Pants"]
    }
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

st.subheader("Genre Preference (0–5, 0 = unknown)")
genre_input = {g: st.slider(g, 0, 5, 0) for g in GENRES}

st.subheader("Color Preference (0–5, 0 = unknown)")
color_input = {c: st.slider(c, 0, 5, 0) for c in COLORS}

# =====================
# 3. Content-Based Scoring
# =====================

def fill_unknown(scores: dict):
    known = [v for v in scores.values() if v > 0]
    avg = sum(known) / len(known) if known else 2.5
    return {k: (v if v > 0 else avg) for k, v in scores.items()}

genre_scores = fill_unknown(genre_input)
color_scores = fill_unknown(color_input)

top_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)[:3]
top_colors = sorted(color_scores.items(), key=lambda x: x[1], reverse=True)

# =====================
# 4. Outfit Generator
# =====================

def generate_outfit(genre, used_colors):
    items = GENRE_ITEMS[genre]
    inner = random.choice(items["inner"])
    outer = random.choice(items["outer"])
    bottom = random.choice(items["bottom"])

    # avoid color duplication
    for c, _ in top_colors:
        if c not in used_colors:
            used_colors.add(c)
            return inner, outer, bottom, c

    c = random.choice(list(COLORS.keys()))
    return inner, outer, bottom, c

# =====================
# 5. Image Generator
# =====================

def generate_image(color_rgb, gender):
    img = Image.new("RGB", (260, 460), "white")
    d = ImageDraw.Draw(img)

    skin = (220, 200, 180)

    # head
    d.ellipse((110, 20, 150, 60), fill=skin)

    # torso
    shoulder = 65 if gender == "Male" else 55
    d.rectangle((130 - shoulder, 70, 130 + shoulder, 200), fill=color_rgb)

    # open outer indication
    d.line((130, 70, 130, 200), fill="white", width=4)

    # legs
    d.rectangle((110, 200, 130, 420), fill=color_rgb)
    d.rectangle((130, 200, 150, 420), fill=color_rgb)

    return img

# =====================
# 6. Output
# =====================

st.header("Recommended Outfits (Top 3 Genres)")

used_colors = set()
cols = st.columns(3)

for i, (genre, score) in enumerate(top_genres):
    with cols[i]:
        inner, outer, bottom, color_name = generate_outfit(genre, used_colors)
        color_rgb = COLORS[color_name]

        st.subheader(f"{genre}")
        st.write(f"**Inner:** {inner}")
        st.write(f"**Outer:** {outer}")
        st.write(f"**Bottom:** {bottom}")
        st.write(f"**Color:** {color_name}")

        img = generate_image(color_rgb, gender)
        st.image(img)

# =====================
# 7. Score Display
# =====================

st.header("Recommendation Scores")
st.subheader("Genre Scores")
st.json(genre_scores)

st.subheader("Color Scores")
st.json(color_scores)
