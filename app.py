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
    img = Image.new("RGB", (500, 600), "#F8F8F8")
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((170, 30), "Today's Outfit", fill="black")

    y = 120
    for key, value in outfit.items():
        draw.rectangle((60, y - 15, 440, y + 35), outline="black", width=2)
        draw.text((80, y), f"{key}: {value}", fill="black")
        y += 80

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
