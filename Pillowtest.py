import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(page_title="Outfit Recommendation", layout="wide")
st.title("Content-Based Outfit Recommendation")

# -----------------------------
# 0. Gender Selection
# -----------------------------
st.header("0️⃣ Select Gender")
gender = st.radio("Gender", ["Male", "Female"])

# -----------------------------
# 1. Genre & Color Definitions
# -----------------------------
GENRES = ["Streetwear", "Casual", "Minimal"]

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

# -----------------------------
# 2. User Input
# -----------------------------
st.header("1️⃣ Rate Your Style Preference (0–5)")
genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}

st.header("2️⃣ Rate Your Color Preference (0–5)")
color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}

# -----------------------------
# 3. Content-Based Completion
# -----------------------------
def complete_scores(scores):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]

# -----------------------------
# 5. Outfit Templates
# -----------------------------
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
    }
}

# -----------------------------
# 6. Outfit Generator
# -----------------------------
def generate_outfit(genre, color, gender):
    parts = OUTFIT_LIBRARY[genre]

    use_skirt = gender == "Female" and random.random() < 0.5

    if use_skirt:
        bottom_item = random.choice(parts["skirt"])
        bottom_type = "Skirt"
    else:
        bottom_item = random.choice(parts["bottom"])
        bottom_type = "Pants"

    return {
        "Genre": genre,
        "Color Theme": color,
        "Inner": f"{color} {random.choice(parts['inner'])}",
        "Outer": f"{color} {random.choice(parts['outer'])}",
        "Bottom": f"{color} {bottom_item}",
        "BottomType": bottom_type
    }

# -----------------------------
# 7. Image Generator
# -----------------------------
import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(page_title="Outfit Recommendation", layout="wide")
st.title("Content-Based Outfit Recommendation")

# -----------------------------
# 0. Gender Selection
# -----------------------------
st.header("0️⃣ Select Gender")
gender = st.radio("Gender", ["Male", "Female"])

# -----------------------------
# 1. Genre & Color Definitions
# -----------------------------
GENRES = ["Streetwear", "Casual", "Minimal"]

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

# -----------------------------
# 2. User Input
# -----------------------------
st.header("1️⃣ Rate Your Style Preference (0–5)")
genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}

st.header("2️⃣ Rate Your Color Preference (0–5)")
color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}

# -----------------------------
# 3. Content-Based Completion
# -----------------------------
def complete_scores(scores):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]

# -----------------------------
# 5. Outfit Templates
# -----------------------------
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
    }
}

# -----------------------------
# 6. Outfit Generator
# -----------------------------
def generate_outfit(genre, color, gender):
    parts = OUTFIT_LIBRARY[genre]

    use_skirt = gender == "Female" and random.random() < 0.5

    if use_skirt:
        bottom_item = random.choice(parts["skirt"])
        bottom_type = "Skirt"
    else:
        bottom_item = random.choice(parts["bottom"])
        bottom_type = "Pants"

    return {
        "Genre": genre,
        "Color Theme": color,
        "Inner": f"{color} {random.choice(parts['inner'])}",
        "Outer": f"{color} {random.choice(parts['outer'])}",
        "Bottom": f"{color} {bottom_item}",
        "BottomType": bottom_type
    }

# -----------------------------
# 7. Image Generator
# -----------------------------
def generate_image(outfit):
    base_color = COLOR_RGB[outfit["Color Theme"]]
    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    skin = (220, 200, 180)
    inner_color = tuple(min(255, c + 35) for c in base_color)
    bottom_color = tuple(max(0, c - 50) for c in base_color)

    d.ellipse([105, 20, 155, 70], fill=skin)
    d.rectangle([120, 70, 140, 95], fill=skin)

    d.polygon([(70, 100), (190, 100), (210, 270), (50, 270)], fill=base_color)
    d.rectangle([95, 120, 165, 250], fill=inner_color)

    if outfit["BottomType"] == "Skirt":
        d.polygon([(85, 260), (175, 260), (200, 350), (60, 350)], fill=bottom_color)
        d.rectangle([110, 350, 130, 400], fill=skin)
        d.rectangle([130, 350, 150, 400], fill=skin)
    else:
        d.rectangle([95, 270, 125, 400], fill=bottom_color)
        d.rectangle([135, 270, 165, 400], fill=bottom_color)

    return img

# -----------------------------
# 8. Generate Outfits
# -----------------------------
st.header("👕 Recommended Outfits")

for i, genre in enumerate(top_genres):
    color = random.choice(top_colors)
    outfit = generate_outfit(genre, color, gender)
    img = generate_image(outfit)
    st.image(img, caption=f"Outfit {i+1}")
    st.write(outfit)


# -----------------------------
# 8. Generate Outfits
# -----------------------------
st.header("👕 Recommended Outfits")

for i, genre in enumerate(top_genres):
    color = random.choice(top_colors)
    outfit = generate_outfit(genre, color, gender)
    img = generate_image(outfit)
    st.image(img, caption=f"Outfit {i+1}")
    st.write(outfit)
