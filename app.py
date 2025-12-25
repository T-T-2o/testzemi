import streamlit as st
import random
from PIL import Image, ImageDraw
import math

st.set_page_config(layout="wide")
st.title("Content-Based Outfit Recommendation (Visual + Logic)")

# =====================
# 1. Definitions
# =====================

GENRES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]
COLORS = ["Black", "Navy", "Beige", "Green", "Red"]
PATTERNS = ["None", "Star"]

COLOR_RGB = {
    "Black": (40, 40, 40),
    "Navy": (50, 70, 110),
    "Beige": (210, 200, 170),
    "Green": (70, 120, 90),
    "Red": (150, 60, 60)
}

# ジャンル → フード有無の傾向
GENRE_HOODIE_PROB = {
    "Streetwear": 0.9,
    "Casual": 0.5,
    "Minimal": 0.2,
    "Techwear": 0.6,
    "Vintage": 0.3,
    "Formal": 0.0
}

# =====================
# 2. User Input
# =====================

st.header("1️⃣ User Attributes")
gender = st.selectbox("Gender", ["Male", "Female"])
body_type = st.selectbox("Body Type", ["Slim", "Average", "Athletic", "Curvy", "Plus-size"])

st.header("2️⃣ Rate Preferences (0–5)")

genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}
color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}
pattern_scores = {p: st.slider(p, 0, 5, 0) for p in PATTERNS}

# =====================
# 3. Content-based Completion
# =====================

def complete_scores(scores):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)
pattern_scores = complete_scores(pattern_scores)

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]
top_patterns = sorted(pattern_scores, key=pattern_scores.get, reverse=True)

# =====================
# 4. Silhouette Params
# =====================

GENDER_PARAMS = {
    "Male": {"shoulder": 1.2, "waist": 0.9, "hip": 0.95},
    "Female": {"shoulder": 0.9, "waist": 0.8, "hip": 1.2}
}

BODY_SCALE = {
    "Slim": 0.85,
    "Average": 1.0,
    "Athletic": 1.1,
    "Curvy": 1.15,
    "Plus-size": 1.3
}

# =====================
# 5. Drawing Utilities
# =====================

def draw_star(draw, cx, cy, r):
    pts = []
    for i in range(10):
        ang = i * math.pi / 5
        rad = r if i % 2 == 0 else r / 2
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill="white")

def draw_pattern(draw, box, pattern):
    if pattern == "Star":
        x1, y1, x2, y2 = box
        for x in range(x1 + 20, x2, 40):
            for y in range(y1 + 20, y2, 40):
                draw_star(draw, x, y, 7)

# =====================
# 6. Image Generator
# =====================

def generate_image(color_name, pattern, hoodie):
    img = Image.new("RGB", (320, 520), "white")
    d = ImageDraw.Draw(img)

    base_color = COLOR_RGB[color_name]
    scale = BODY_SCALE[body_type]
    shape = GENDER_PARAMS[gender]

    shoulder = 70 * shape["shoulder"] * scale
    waist = 55 * shape["waist"] * scale
    hip = 65 * shape["hip"] * scale
    center = 160

    # Head
    d.ellipse((130, 20, 190, 80), fill=(220, 200, 180))

    # Torso (polygon)
    torso = [
        (center - shoulder, 90),
        (center + shoulder, 90),
        (center + waist, 200),
        (center + hip, 320),
        (center - hip, 320),
        (center - waist, 200)
    ]
    d.polygon(torso, fill=base_color, outline="black")

    # Pattern
    draw_pattern(d, (center - hip, 90, center + hip, 320), pattern)

    # Hoodie
    if hoodie:
        d.pieslice(
            (center - 55, 60, center + 55, 130),
            180, 360,
            fill=base_color,
            outline="black",
            width=3
        )

    # Legs
    d.rectangle((center - 45, 320, center - 5, 470), fill=base_color)
    d.rectangle((center + 5, 320, center + 45, 470), fill=base_color)

    return img

# =====================
# 7. Output (3 Outfits)
# =====================

st.header("👕 Recommended Outfits (Content-Based)")

used_colors = []

for i, genre in enumerate(top_genres):

    # color (avoid duplication)
    color = random.choice(top_colors)
    if color in used_colors and len(top_colors) > 1:
        color = random.choice([c for c in top_colors if c not in used_colors])
    used_colors.append(color)

    # pattern
    pattern = top_patterns[0]

    # hoodie probability by genre
    hoodie = random.random() < GENRE_HOODIE_PROB[genre]

    img = generate_image(color, pattern, hoodie)

    col1, col2 = st.columns([1, 1.4])
    with col1:
        st.image(img, caption=f"Outfit {i+1}")

    with col2:
        st.subheader(f"Outfit {i+1}")
        st.write(f"**Genre:** {genre}")
        st.write(f"**Color:** {color}")
        st.write(f"**Pattern:** {pattern}")
        st.write(f"**Hoodie:** {'Yes' if hoodie else 'No'}")
        st.write(f"**Gender:** {gender}")
        st.write(f"**Body Type:** {body_type}")

# =====================
# 8. Final Scores
# =====================

st.header("📊 Final Recommendation Scores")
st.subheader("Genre Scores")
st.json(genre_scores)

st.subheader("Color Scores")
st.json(color_scores)

st.subheader("Pattern Scores")
st.json(pattern_scores)
