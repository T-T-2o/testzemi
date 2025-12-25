import streamlit as st
import random
from PIL import Image, ImageDraw

# ===============================
# Page Config
# ===============================
st.set_page_config(page_title="Outfit Recommender", layout="wide")
st.title("👕 Content-Based Outfit Recommendation")

# ===============================
# Definitions
# ===============================

GENRES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]
COLORS = ["Black", "White", "Gray", "Navy", "Brown", "Beige", "Green", "Red"]

COLOR_RGB = {
    "Black": (30, 30, 30),
    "White": (240, 240, 240),
    "Gray": (160, 160, 160),
    "Navy": (40, 60, 100),
    "Brown": (120, 80, 50),
    "Beige": (210, 200, 170),
    "Green": (60, 120, 80),
    "Red": (160, 50, 50)
}

OUTFIT_LIBRARY = {
    "Streetwear": {
        "inner": ["Graphic Tee", "Long Sleeve Tee"],
        "outer": ["Hoodie", "Zip Hoodie"],
        "bottom": ["Cargo Pants", "Wide Pants"]
    },
    "Casual": {
        "inner": ["Plain T-Shirt", "Knit"],
        "outer": ["Cardigan", "Light Jacket"],
        "bottom": ["Denim", "Chinos"]
    },
    "Minimal": {
        "inner": ["Plain Tee"],
        "outer": ["Tailored Jacket"],
        "bottom": ["Slim Slacks"]
    },
    "Techwear": {
        "inner": ["Functional Tee"],
        "outer": ["Shell Jacket"],
        "bottom": ["Tech Pants"]
    },
    "Vintage": {
        "inner": ["Retro Tee"],
        "outer": ["Denim Jacket"],
        "bottom": ["Straight Jeans"]
    },
    "Formal": {
        "inner": ["Dress Shirt"],
        "outer": ["Blazer"],
        "bottom": ["Slacks"]
    }
}

# ===============================
# 1. User Input
# ===============================

st.header("1️⃣ Rate Your Style Preference (0–5)")
genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}

st.header("2️⃣ Rate Your Color Preference (0–5)")
color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}

# ===============================
# 2. Content-Based Completion
# ===============================

def complete_scores(scores):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)

# ===============================
# 3. Select Top Genres & Colors
# ===============================

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]

# ===============================
# 4. Outfit Generator
# ===============================

def generate_outfit(genre, color):
    parts = OUTFIT_LIBRARY[genre]
    return {
        "Genre": genre,
        "Color Theme": color,
        "Inner": f"{color} {random.choice(parts['inner'])}",
        "Outer": f"{color} {random.choice(parts['outer'])}",
        "Bottom": f"{color} {random.choice(parts['bottom'])}"
    }

# ===============================
# 5. Image Generator (Colorized)
# ===============================

def generate_image(outfit):
    base = COLOR_RGB[outfit["Color Theme"]]
    inner = tuple(min(255, c + 40) for c in base)
    bottom = tuple(max(0, c - 40) for c in base)

    img = Image.new("RGB", (260, 440), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # Head
    d.ellipse([100, 20, 160, 80], fill=(220, 200, 180))

    # Outer
    d.rectangle([60, 100, 200, 260], fill=base, outline="black", width=3)

    # Hoodie hood
    if "Hoodie" in outfit["Outer"]:
        d.arc([80, 80, 180, 140], 0, 180, fill="black", width=4)

    # Inner
    d.rectangle([80, 120, 180, 240], fill=inner, outline="black", width=2)

    # Graphic Tee logo
    if "Graphic Tee" in outfit["Inner"]:
        d.rectangle([110, 160, 150, 200], fill=(255, 255, 255))

    # Bottom
    d.rectangle([90, 260, 170, 400], fill=bottom, outline="black", width=3)

    return img

# ===============================
# 6. Generate 3 Outfits (No Color Duplication)
# ===============================

st.header("👕 Recommended Outfits")

used_colors = []

for i, genre in enumerate(top_genres):
    color = random.choice(top_colors)

    if color in used_colors and len(top_colors) > 1:
        color = random.choice([c for c in top_colors if c not in used_colors])

    used_colors.append(color)

    outfit = generate_outfit(genre, color)
    img = generate_image(outfit)

    col1, col2 = st.columns([1, 1.6])

    with col1:
        st.image(img, caption=f"Outfit {i+1}")

    with col2:
        st.subheader(f"Outfit {i+1} Details")
        st.write(f"**Genre:** {outfit['Genre']}")
        st.write(f"**Color Theme:** {outfit['Color Theme']}")
        st.write(f"👕 Inner: {outfit['Inner']}")
        st.write(f"🧥 Outer: {outfit['Outer']}")
        st.write(f"👖 Bottom: {outfit['Bottom']}")

# ===============================
# 7. Final Scores
# ===============================

st.header("📊 Recommendation Scores")
st.subheader("Genre Scores")
st.json(genre_scores)
st.subheader("Color Scores")
st.json(color_scores)
