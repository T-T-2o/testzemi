import streamlit as st
import random
from PIL import Image, ImageDraw

# =========================
# 1. Genres
# =========================
GENRES = ["Casual", "Street", "Mode", "Minimal", "Formal", "Outdoor"]

# =========================
# 2. Similarity (content-based)
# =========================
SIMILARITY = {
    "Casual":   {"Street": 0.7, "Minimal": 0.6, "Outdoor": 0.5},
    "Street":   {"Casual": 0.7, "Mode": 0.6},
    "Mode":     {"Street": 0.6, "Formal": 0.7, "Minimal": 0.5},
    "Minimal":  {"Casual": 0.6, "Mode": 0.5, "Formal": 0.6},
    "Formal":   {"Mode": 0.7, "Minimal": 0.6},
    "Outdoor":  {"Casual": 0.5}
}

# =========================
# 3. Color palettes (HEX)
# =========================
COLORS = {
    "Casual": {
        "inner": ["#FFFFFF", "#EAEAEA", "#D6E4F0"],
        "outer": ["#C8D6B9", "#B0C4DE"],
        "bottom": ["#4F6D7A", "#6B7A8F"],
        "shoes": ["#FFFFFF", "#333333"]
    },
    "Street": {
        "inner": ["#000000", "#5A5A5A"],
        "outer": ["#2F4F4F", "#556B2F"],
        "bottom": ["#3B3B3B", "#2E2E2E"],
        "shoes": ["#000000"]
    },
    "Mode": {
        "inner": ["#111111", "#2B2B2B"],
        "outer": ["#1A1A1A"],
        "bottom": ["#222222"],
        "shoes": ["#000000"]
    },
    "Minimal": {
        "inner": ["#FFFFFF", "#F2F2F2"],
        "outer": ["#DCDCDC"],
        "bottom": ["#BEBEBE"],
        "shoes": ["#888888"]
    },
    "Formal": {
        "inner": ["#FFFFFF"],
        "outer": ["#1C1C3C", "#000000"],
        "bottom": ["#1C1C3C"],
        "shoes": ["#000000"]
    },
    "Outdoor": {
        "inner": ["#D2B48C"],
        "outer": ["#556B2F", "#6B8E23"],
        "bottom": ["#8B7D6B"],
        "shoes": ["#4B3621"]
    }
}

# =========================
# 4. Outfit structure
# =========================
OUTFIT_DB = {
    "Casual":   ["T-shirt", "Cardigan", "Denim", "Sneakers"],
    "Street":   ["Graphic Tee", "Hoodie", "Cargo Pants", "High-top Sneakers"],
    "Mode":     ["High-neck Top", "Tailored Jacket", "Slacks", "Leather Shoes"],
    "Minimal":  ["Plain Shirt", "Coat", "Straight Pants", "Simple Sneakers"],
    "Formal":   ["Dress Shirt", "Suit Jacket", "Suit Pants", "Oxford Shoes"],
    "Outdoor":  ["Thermal Top", "Mountain Jacket", "Utility Pants", "Hiking Boots"]
}

# =========================
# 5. Content-based completion
# =========================
def complete_scores(user_scores):
    completed = user_scores.copy()
    for g, v in completed.items():
        if v is None:
            s, w = 0, 0
            for k, vk in user_scores.items():
                if vk is not None and k in SIMILARITY.get(g, {}):
                    weight = SIMILARITY[g][k]
                    s += vk * weight
                    w += weight
            completed[g] = round(s / w, 2) if w else 0
    return completed

# =========================
# 6. Outfit generation
# =========================
def generate_outfit(genre):
    items = OUTFIT_DB[genre]
    colors = COLORS[genre]

    return {
        "Genre": genre,
        "Inner": items[0],
        "Outer": items[1],
        "Bottom": items[2],
        "Shoes": items[3],
        "Color": {
            "Inner": random.choice(colors["inner"]),
            "Outer": random.choice(colors["outer"]),
            "Bottom": random.choice(colors["bottom"]),
            "Shoes": random.choice(colors["shoes"])
        }
    }

# =========================
# 7. Image generation (color-aware)
# =========================
def generate_outfit_image(outfit):
    img = Image.new("RGB", (300, 500), "#F5F5F5")
    d = ImageDraw.Draw(img)

    # Head
    d.ellipse((130, 30, 170, 70), fill="#333333")

    # Inner
    d.rectangle((120, 80, 180, 200), fill=outfit["Color"]["Inner"])

    # Outer (open front)
    d.rectangle((100, 80, 120, 230), fill=outfit["Color"]["Outer"])
    d.rectangle((180, 80, 200, 230), fill=outfit["Color"]["Outer"])

    # Bottom
    d.rectangle((120, 200, 145, 360), fill=outfit["Color"]["Bottom"])
    d.rectangle((155, 200, 180, 360), fill=outfit["Color"]["Bottom"])

    # Shoes
    d.rectangle((115, 360, 145, 380), fill=outfit["Color"]["Shoes"])
    d.rectangle((155, 360, 185, 380), fill=outfit["Color"]["Shoes"])

    d.text((10, 10), outfit["Genre"], fill="black")
    return img

# =========================
# 8. Streamlit UI
# =========================
st.title("Color-Rich Outfit Recommendation")

user_scores = {}
for g in GENRES:
    v = st.selectbox(g, ["Unknown", 0, 1, 2, 3, 4, 5], key=g)
    user_scores[g] = None if v == "Unknown" else v

if st.button("Generate"):
    scores = complete_scores(user_scores)
    top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

    for genre, score in top3:
        outfit = generate_outfit(genre)
        img = generate_outfit_image(outfit)

        st.subheader(f"{genre} (score: {score})")
        st.image(img)
        st.json(outfit)
