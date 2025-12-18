import streamlit as st
import random
from PIL import Image, ImageDraw

# ----------------------
# Page config
# ----------------------
st.set_page_config(
    page_title="Outfit Generator",
    page_icon="👕",
    layout="centered"
)

# ----------------------
# Clothing data (EN)
# ----------------------
tops = [
    "White T-shirt", "Black T-shirt", "Shirt",
    "Hoodie", "Knit", "Jacket"
]

bottoms = [
    "Denim Pants", "Black Slacks",
    "Chino Pants", "Short Pants"
]

outerwear = [
    "None", "Cardigan", "Coat", "Down Jacket"
]

shoes = [
    "Sneakers", "Leather Shoes",
    "Loafers", "Boots", "Sandals"
]

accessories = [
    "None", "Watch", "Necklace",
    "Cap", "Backpack"
]

# ----------------------
# Outfit generation
# ----------------------
def generate_outfit(season):
    if season == "Summer":
        tops_season = ["White T-shirt", "Black T-shirt", "Short Sleeve Shirt"]
        outer = ["None"]
    elif season == "Winter":
        tops_season = ["Knit", "Hoodie"]
        outer = ["Coat", "Down Jacket"]
    elif season in ["Spring", "Autumn"]:
        tops_season = ["Shirt", "Hoodie", "Jacket"]
        outer = ["Cardigan", "Jacket"]
    else:
        tops_season = tops
        outer = outerwear

    return {
        "Top": random.choice(tops_season),
        "Bottom": random.choice(bottoms),
        "Outer": random.choice(outer),
        "Shoes": random.choice(shoes),
        "Accessory": random.choice(accessories)
    }

# ----------------------
# Image generation
# ----------------------
def generate_outfit_image(outfit):
    img = Image.new("RGB", (400, 600), "#F0F0F0")
    draw = ImageDraw.Draw(img)

    # ---- Head ----
    draw.ellipse((170, 40, 230, 100), fill="#FFD6A5", outline="black")

    # ---- Top (Upper body) ----
    top_color = "#A3CEF1"   # blue-ish
    draw.rectangle((140, 110, 260, 260), fill=top_color, outline="black")

    # ---- Bottom (Lower body) ----
    bottom_color = "#6C757D"  # gray
    draw.rectangle((140, 260, 260, 400), fill=bottom_color, outline="black")

    # ---- Legs ----
    draw.rectangle((150, 400, 185, 520), fill=bottom_color, outline="black")
    draw.rectangle((215, 400, 250, 520), fill=bottom_color, outline="black")

    # ---- Shoes ----
    draw.rectangle((145, 520, 190, 560), fill="#333333", outline="black")
    draw.rectangle((210, 520, 255, 560), fill="#333333", outline="black")

    # ---- Labels (small text) ----
    draw.text((10, 10), "Visual Outfit Preview", fill="black")

    return img


# ----------------------
# Streamlit UI
# ----------------------
st.title("👕 Outfit Generator")
st.write("Click the button to generate a random outfit and its image.")

season = st.selectbox(
    "Select season",
    ["All", "Spring", "Summer", "Autumn", "Winter"]
)

if st.button("Generate Outfit"):
    outfit = generate_outfit(season)

    st.subheader("Outfit Details")
    for k, v in outfit.items():
        st.write(f"**{k}**: {v}")

    st.subheader("Outfit Image")
    img = generate_outfit_image(outfit)
    st.image(img, use_container_width=True)

    st.success("New outfit generated!")
