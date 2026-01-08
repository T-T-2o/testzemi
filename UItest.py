import streamlit as st
import random
from PIL import Image, ImageDraw

# =============================
# Page Config
# =============================
st.set_page_config(page_title="Outfit Recommendation", layout="wide")
st.title("Content-Based Outfit Recommendation")

# =============================
# Layout
# =============================
left, right = st.columns([1, 2])

# =============================
# 1. Genre & Color Definitions
# =============================
GENRES = [
    "Streetwear", "Casual", "Minimal",
    "Techwear", "Vintage", "Formal"
]

COLORS = [
    "Black", "White", "Gray", "Navy",
    "Brown", "Beige", "Green", "Red"
]

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

# =============================
# LEFT : User Preferences
# =============================
with left:
    st.header("🧑‍💼 Your Preferences")

    st.subheader("Gender / Options")
    gender = st.radio("Gender", ["Male", "Female"])
    use_outer = st.checkbox("Wear Outer", value=True)

    st.subheader("Style Preference (0–5)")
    genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}

    st.subheader("Color Preference (0–5)")
    color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}

def complete_scores(scores):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]

# =============================
# Outfit Library
# =============================
OUTFIT_LIBRARY = {
    "Streetwear": {
        "inner": ["Graphic Tee", "Long Sleeve Tee"],
        "outer": ["Hoodie", "Zip Hoodie"],
        "bottom": ["Wide Pants", "Cargo Pants"],
        "skirt": ["Mini Skirt", "Pleated Skirt"]
    },
    "Casual": {
        "inner": ["Plain T-Shirt", "Knit"],
        "outer": ["Cardigan", "Light Jacket"],
        "bottom": ["Denim", "Chinos"],
        "skirt": ["Flare Skirt", "Long Skirt"]
    },
    "Minimal": {
        "inner": ["Plain Tee"],
        "outer": ["Tailored Jacket"],
        "bottom": ["Slim Slacks"],
        "skirt": ["Straight Skirt"]
    },
    "Techwear": {
        "inner": ["Functional Tee"],
        "outer": ["Shell Jacket"],
        "bottom": ["Tech Pants"],
        "skirt": ["Tech Skirt"]
    },
    "Vintage": {
        "inner": ["Retro Tee"],
        "outer": ["Denim Jacket"],
        "bottom": ["Straight Jeans"],
        "skirt": ["Retro Skirt"]
    },
    "Formal": {
        "inner": ["Dress Shirt"],
        "outer": ["Blazer"],
        "bottom": ["Slacks"],
        "skirt": ["Tight Skirt"]
    }
}

# =============================
# Outfit Generator
# =============================
def generate_outfit(genre, color, gender, use_outer):
    parts = OUTFIT_LIBRARY[genre]
    use_skirt = gender == "Female" and random.random() < 0.5

    bottom_item = random.choice(parts["skirt"] if use_skirt else parts["bottom"])

    return {
        "Genre": genre,
        "Color Theme": color,
        "Inner": f"{color} {random.choice(parts['inner'])}",
        "Outer": f"{color} {random.choice(parts['outer'])}" if use_outer else None,
        "HasOuter": use_outer,
        "Bottom": f"{color} {bottom_item}",
        "BottomType": "Skirt" if use_skirt else "Pants"
    }

# =============================
# Image Generator
# =============================
def generate_image(outfit):
    base = COLOR_RGB[outfit["Color Theme"]]
    skin = (220, 200, 180)
    inner = tuple(min(255, c + 35) for c in base)
    bottom = tuple(max(0, c - 50) for c in base)

    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    # Head
    d.ellipse([105, 20, 155, 70], fill=skin, outline="black")
    d.rectangle([120, 70, 140, 95], fill=skin, outline="black")

    if outfit["HasOuter"]:
        d.rectangle([50, 120, 80, 260], fill=base, outline="black")
        d.rectangle([180, 120, 210, 260], fill=base, outline="black")
        d.polygon([(70, 100), (190, 100), (210, 270), (50, 270)],
                  fill=base, outline="black")
        d.rectangle([95, 120, 165, 250], fill=inner, outline="black")

        if outfit["Outer"] and "Hoodie" in outfit["Outer"]:
            d.arc([85, 75, 175, 145], start=0, end=180, fill="black", width=4)
    else:
        d.rectangle([75, 100, 185, 260], fill=inner, outline="black")
        d.rectangle([55, 120, 75, 260], fill=inner, outline="black")
        d.rectangle([185, 120, 205, 260], fill=inner, outline="black")

    if outfit["BottomType"] == "Skirt":
        d.polygon([(85, 260), (175, 260), (200, 350), (60, 350)],
                  fill=bottom, outline="black")
        d.rectangle([110, 350, 130, 400], fill=skin, outline="black")
        d.rectangle([130, 350, 150, 400], fill=skin, outline="black")
    else:
        d.rectangle([95, 270, 125, 400], fill=bottom, outline="black")
        d.rectangle([135, 270, 165, 400], fill=bottom, outline="black")

    d.rectangle([90, 400, 130, 420], fill=(40, 40, 40))
    d.rectangle([130, 400, 170, 420], fill=(40, 40, 40))

    return img

# =============================
# RIGHT : Recommendations
# =============================
with right:
    st.header("👕 Recommended Outfits")

    used_colors = []

    for i, genre in enumerate(top_genres):
        color = random.choice([c for c in top_colors if c not in used_colors] or top_colors)
        used_colors.append(color)

        outfit = generate_outfit(genre, color, gender, use_outer)
        img = generate_image(outfit)

        st.subheader(f"Outfit {i + 1}")
        st.image(img, width=260)

        st.write(f"**Genre:** {outfit['Genre']}")
        st.write(f"**Color Theme:** {outfit['Color Theme']}")
        st.write(f"👕 Inner: {outfit['Inner']}")
        if outfit["Outer"]:
            st.write(f"🧥 Outer: {outfit['Outer']}")
        st.write(f"👖 Bottom: {outfit['Bottom']}")
        st.divider()
