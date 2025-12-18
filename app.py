import streamlit as st
import random
from PIL import Image, ImageDraw

# ======================
# Page config
# ======================
st.set_page_config(
    page_title="Outfit Generator",
    page_icon="👕",
    layout="centered"
)

# ======================
# Clothing data
# ======================
tops = {
    "White T-shirt": "#FFFFFF",
    "Black T-shirt": "#222222",
    "Shirt": "#E0E0E0",
    "Hoodie": "#7A9E9F",
    "Knit": "#C97C5D",
    "Jacket": "#5F6CAF"
}

bottoms = {
    "Denim Pants": "#4F6D7A",
    "Black Slacks": "#2E2E2E",
    "Chino Pants": "#C2B280",
    "Short Pants": "#A5A58D"
}

outerwear = {
    "None": None,
    "Cardigan": "#B5838D",
    "Coat": "#6D6875",
    "Down Jacket": "#495057"
}

shoes = {
    "Sneakers": "#FFFFFF",
    "Leather Shoes": "#3A1F04",
    "Boots": "#5A3825",
    "Sandals": "#D6CCC2"
}

# ======================
# Outfit generation
# ======================
def generate_outfit(season):
    top = random.choice(list(tops.keys()))
    bottom = random.choice(list(bottoms.keys()))
    outer = random.choice(list(outerwear.keys()))
    shoe = random.choice(list(shoes.keys()))

    return {
        "Top": top,
        "Bottom": bottom,
        "Outer": outer,
        "Shoes": shoe
    }

# ======================
# Image generation
# ======================
def generate_outfit_image(outfit):
    img = Image.new("RGB", (400, 650), "#F2F2F2")
    draw = ImageDraw.Draw(img)

    # ---- Head ----
    draw.ellipse((170, 30, 230, 90), fill="#FFD6A5", outline="black")

    # ---- Top ----
    draw.rectangle(
        (140, 100, 260, 260),
        fill=tops[outfit["Top"]],
        outline="black"
    )

    # ---- Outer (layered) ----
    if outfit["Outer"] != "None":
        draw.rectangle(
            (130, 95, 270, 270),
            fill=outerwear[outfit["Outer"]],
            outline="black"
        )

    # ---- Bottom ----
    draw.rectangle(
        (140, 260, 260, 420),
        fill=bottoms[outfit["Bottom"]],
        outline="black"
    )

    # ---- Legs ----
    draw.rectangle((150, 420, 185, 550), fill=bottoms[outfit["Bottom"]], outline="black")
    draw.rectangle((215, 420, 250, 550), fill=bottoms[outfit["Bottom"]], outline="black")

    # ---- Shoes ----
    draw.rectangle((145, 550, 190, 600), fill=shoes[outfit["Shoes"]], outline="black")
    draw.rectangle((210, 550, 255, 600), fill=shoes[outfit["Shoes"]], outline="black")

    # ---- Title ----
    draw.text((120, 610), "Outfit Preview", fill="black")

    return img

# ======================
# UI
# ======================
st.title("👕 Outfit Generator")
st.write("Generate a random outfit with a visual preview.")

if st.button("Generate Outfit"):
    outfit = generate_outfit("All")

    st.subheader("Outfit Details")
    for k, v in outfit.items():
        st.write(f"**{k}**: {v}")

    st.subheader("Outfit Image")
    st.image(generate_outfit_image(outfit), use_container_width=True)

    st.success("Outfit generated successfully!")
