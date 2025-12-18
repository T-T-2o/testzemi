import streamlit as st
import random
from PIL import Image, ImageDraw

# =========================
# 1. Genre definition
# =========================
GENRES = ["Casual", "Street", "Mode", "Minimal", "Formal", "Outdoor"]

# =========================
# 2. Genre similarity (content-based)
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
# 3. Outfit database by genre
# =========================
OUTFIT_DB = {
    "Casual": {
        "inner": ["T-shirt", "Sweatshirt"],
        "outer": ["Cardigan", "Light Jacket", "None"],
        "bottom": ["Denim", "Chinos"],
        "shoes": ["Sneakers"],
        "colors": ["White", "Gray", "Navy"]
    },
    "Street": {
        "inner": ["Graphic Tee", "Oversized Tee"],
        "outer": ["Hoodie", "Bomber Jacket"],
        "bottom": ["Cargo Pants", "Wide Denim"],
        "shoes": ["High-top Sneakers"],
        "colors": ["Black", "Khaki", "Red"]
    },
    "Mode": {
        "inner": ["Slim Shirt", "High-neck Top"],
        "outer": ["Tailored Jacket"],
        "bottom": ["Slacks"],
        "shoes": ["Leather Shoes"],
        "colors": ["Black", "Dark Gray"]
    },
    "Minimal": {
        "inner": ["Plain Shirt", "Knit"],
        "outer": ["None", "Coat"],
        "bottom": ["Straight Pants"],
        "shoes": ["Simple Sneakers"],
        "colors": ["White", "Beige", "Gray"]
    },
    "Formal": {
        "inner": ["Dress Shirt"],
        "outer": ["Suit Jacket"],
        "bottom": ["Suit Pants"],
        "shoes": ["Oxford Shoes"],
        "colors": ["Navy", "Black"]
    },
    "Outdoor": {
        "inner": ["Thermal Top"],
        "outer": ["Mountain Jacket"],
        "bottom": ["Utility Pants"],
        "shoes": ["Hiking Boots"],
        "colors": ["Olive", "Brown"]
    }
}

# =========================
# 4. Preference completion
# =========================
def complete_scores(user_scores):
    completed = user_scores.copy()
    for g, score in completed.items():
        if score is None:
            total, weight = 0, 0
            for k, v in user_scores.items():
                if v is not None and k in SIMILARITY.get(g, {}):
                    w = SIMILARITY[g][k]
                    total += v * w
                    weight += w
            completed[g] = round(total / weight, 2) if weight else 0
    return completed

# =========================
# 5. Outfit generation
# =========================
def generate_outfit(genre):
    base = OUTFIT_DB[genre]
    return {
        "Genre": genre,
        "Inner": random.choice(base["inner"]),
        "Outer": random.choice(base["outer"]),
        "Bottom": random.choice(base["bottom"]),
        "Shoes": random.choice(base["shoes"]),
        "Color": random.choice(base["colors"])
    }

# =========================
# 6. Image generation (layered silhouette)
# =========================
def generate_outfit_image(outfit):
    img = Image.new("RGB", (300, 500), "#F5F5F5")
    d = ImageDraw.Draw(img)

    # Head
    d.ellipse((130, 30, 170, 70), fill="black")

    # Inner
    d.rectangle((120, 80, 180, 200), fill="#CCCCCC")

    # Outer (front open)
    if outfit["Outer"] != "None":
        d.rectangle((100, 80, 120, 220), fill="#888888")
        d.rectangle((180, 80, 200, 220), fill="#888888")

    # Bottom
    d.rectangle((120, 200, 145, 350), fill="#555555")
    d.rectangle((155, 200, 180, 350), fill="#555555")

    # Shoes
    d.rectangle((115, 350, 145, 370), fill="black")
    d.rectangle((155, 350, 185, 370), fill="black")

    # Label
    d.text((10, 10), outfit["Genre"], fill="black")

    return img

# =========================
# 7. Streamlit UI
# =========================
st.title("Content-Based Outfit Recommendation")

st.header("Rate Your Style Preference (0–5)")
user_scores = {}
for g in GENRES:
    v = st.selectbox(g, ["Unknown", 0, 1, 2, 3, 4, 5], key=g)
    user_scores[g] = None if v == "Unknown" else v

if st.button("Generate Outfit"):
    scores = complete_scores(user_scores)
    top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

    st.subheader("Top 3 Recommended Outfits")

    for genre, score in top3:
        outfit = generate_outfit(genre)
        img = generate_outfit_image(outfit)

        st.markdown(f"### {genre} (score: {score})")
        st.image(img)
        st.json(outfit)
