import streamlit as st
import random
from PIL import Image, ImageDraw

# =========================
# 1. Definitions
# =========================
GENRES = ["Casual", "Street", "Mode", "Minimal", "Formal", "Outdoor"]
COLOR_STYLES = ["Monochrome", "Neutral", "Warm", "Cool", "Earth"]

# =========================
# 2. Similarity matrices
# =========================
GENRE_SIM = {
    "Casual": {"Street": 0.7, "Minimal": 0.6, "Outdoor": 0.5},
    "Street": {"Casual": 0.7, "Mode": 0.6},
    "Mode": {"Street": 0.6, "Formal": 0.7, "Minimal": 0.5},
    "Minimal": {"Casual": 0.6, "Mode": 0.5, "Formal": 0.6},
    "Formal": {"Mode": 0.7, "Minimal": 0.6},
    "Outdoor": {"Casual": 0.5}
}

COLOR_SIM = {
    "Monochrome": {"Neutral": 0.7},
    "Neutral": {"Monochrome": 0.7, "Earth": 0.6},
    "Warm": {"Earth": 0.7},
    "Cool": {"Monochrome": 0.6},
    "Earth": {"Warm": 0.7, "Neutral": 0.6}
}

# =========================
# 3. Color palettes
# =========================
COLOR_PALETTE = {
    "Monochrome": {"inner": ["#000000", "#2B2B2B"], "outer": ["#1A1A1A"], "bottom": ["#222222"], "shoes": ["#000000"]},
    "Neutral": {"inner": ["#FFFFFF", "#F2F2F2"], "outer": ["#DCDCDC"], "bottom": ["#BEBEBE"], "shoes": ["#888888"]},
    "Warm": {"inner": ["#F5CBA7"], "outer": ["#DC7633"], "bottom": ["#AF601A"], "shoes": ["#6E2C00"]},
    "Cool": {"inner": ["#AED6F1"], "outer": ["#5DADE2"], "bottom": ["#2E86C1"], "shoes": ["#1B4F72"]},
    "Earth": {"inner": ["#D2B48C"], "outer": ["#6B8E23"], "bottom": ["#8B7D6B"], "shoes": ["#4B3621"]}
}

# =========================
# 4. Outfit templates
# =========================
OUTFIT_DB = {
    "Casual": ["T-shirt", "Cardigan", "Denim", "Sneakers"],
    "Street": ["Graphic Tee", "Hoodie", "Cargo Pants", "High-top Sneakers"],
    "Mode": ["High-neck Top", "Tailored Jacket", "Slacks", "Leather Shoes"],
    "Minimal": ["Plain Shirt", "Coat", "Straight Pants", "Simple Sneakers"],
    "Formal": ["Dress Shirt", "Suit Jacket", "Suit Pants", "Oxford Shoes"],
    "Outdoor": ["Thermal Top", "Mountain Jacket", "Utility Pants", "Hiking Boots"]
}

# =========================
# 5. Content-based completion
# =========================
def complete_scores(scores, similarity):
    completed = scores.copy()
    for k, v in completed.items():
        if v is None:
            s, w = 0, 0
            for kk, vv in scores.items():
                if vv is not None and kk in similarity.get(k, {}):
                    weight = similarity[k][kk]
                    s += vv * weight
                    w += weight
            completed[k] = round(s / w, 2) if w else 0
    return completed

# =========================
# 6. Outfit generation
# =========================
def generate_outfit(genre, color_style):
    palette = COLOR_PALETTE[color_style]
    items = OUTFIT_DB[genre]

    return {
        "Genre": genre,
        "ColorStyle": color_style,
        "Inner": items[0],
        "Outer": items[1],
        "Bottom": items[2],
        "Shoes": items[3],
        "Colors": {
            "Inner": random.choice(palette["inner"]),
            "Outer": random.choice(palette["outer"]),
            "Bottom": random.choice(palette["bottom"]),
            "Shoes": random.choice(palette["shoes"])
        }
    }

# =========================
# 7. Image generation
# =========================
def generate_image(outfit):
    img = Image.new("RGB", (300, 500), "#F5F5F5")
    d = ImageDraw.Draw(img)

    d.ellipse((130, 30, 170, 70), fill="#333333")
    d.rectangle((120, 80, 180, 200), fill=outfit["Colors"]["Inner"])
    d.rectangle((100, 80, 120, 230), fill=outfit["Colors"]["Outer"])
    d.rectangle((180, 80, 200, 230), fill=outfit["Colors"]["Outer"])
    d.rectangle((120, 200, 145, 360), fill=outfit["Colors"]["Bottom"])
    d.rectangle((155, 200, 180, 360), fill=outfit["Colors"]["Bottom"])
    d.rectangle((115, 360, 145, 380), fill=outfit["Colors"]["Shoes"])
    d.rectangle((155, 360, 185, 380), fill=outfit["Colors"]["Shoes"])

    d.text((10, 10), f"{outfit['Genre']} / {outfit['ColorStyle']}", fill="black")
    return img

# =========================
# 8. Streamlit UI
# =========================
st.title("Content-Based Outfit Recommendation (3 Suggestions)")

st.header("Style Preference (0–5)")
genre_scores = {
    g: None if (v := st.selectbox(g, ["Unknown", 0, 1, 2, 3, 4, 5], key=f"g_{g}")) == "Unknown" else v
    for g in GENRES
}

st.header("Color Preference (0–5)")
color_scores = {
    c: None if (v := st.selectbox(c, ["Unknown", 0, 1, 2, 3, 4, 5], key=f"c_{c}")) == "Unknown" else v
    for c in COLOR_STYLES
}

if st.button("Generate Outfits"):
    genre_result = complete_scores(genre_scores, GENRE_SIM)
    color_result = complete_scores(color_scores, COLOR_SIM)

    top_genres = sorted(genre_result, key=genre_result.get, reverse=True)[:3]
    top_colors = sorted(color_result, key=color_result.get, reverse=True)[:2]

    st.subheader("Recommended Outfits")

    for i, genre in enumerate(top_genres):
        color_style = random.choice(top_colors)
        outfit = generate_outfit(genre, color_style)
        img = generate_image(outfit)

        st.markdown(f"### Outfit {i+1}")
        st.image(img)
        st.json(outfit)

