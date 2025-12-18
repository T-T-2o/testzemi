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
# name + color name + color code
# ======================
tops = [
    {"name": "White T-shirt", "color_name": "White", "color_code": "#FFFFFF"},
    {"name": "Black T-shirt", "color_name": "Black", "color_code": "#222222"},
    {"name": "Shirt", "color_name": "Light Gray", "color_code": "#E0E0E0"},
    {"name": "Hoodie", "color_name": "Blue Green", "color_code": "#7A9E9F"},
    {"name": "Knit", "color_name": "Brown", "color_code": "#C97C5D"},
    {"name": "Jacket", "color_name": "Navy", "color_code": "#5F6CAF"},
]

bottoms = [
    {"name": "Denim Pants", "color_name": "Indigo", "color_code": "#4F6D7A"},
    {"name": "Black Slacks", "color_name": "Black", "color_code": "#2E2E2E"},
    {"name": "Chino Pants", "color_name": "Beige", "color_code": "#C2B280"},
    {"name": "Short Pants", "color_name": "Khaki", "color_code": "#A5A58D"},
]

outerwear = [
    {"name": "None", "color_name": "-", "color_code": None},
    {"name": "Cardigan", "color_name": "Rose Brown", "color_code": "#B5838D"},
    {"name": "Coat", "color_name": "Dark Gray", "color_code": "#6D6875"},
    {"name": "Down Jacket", "color_name": "Charcoal", "color_code": "#495057"},
]

shoes = [
    {"name": "Sneakers", "color_name": "White", "color_code": "#FFFFFF"},
    {"name": "Leather Shoes", "color_name": "Dark Brown", "color_code": "#3A1F04"},
    {"name": "Boots", "color_name": "Brown", "color_code": "#5A3825"},
    {"name": "Sandals", "color_name": "Ivory", "color_code": "#D6CCC2"},
]

# ======================
# Outfit generation
# ======================
def generate_outfit():
    return {
        "Top": random.choice(tops),
        "Bottom": random.choice(bottoms),
        "Outer": random.choice(outerwear),
        "Shoes": random.choice(shoes),
    }

# ======================
# Image generation
# ======================
def generate_outfit_image(outfit):
    img = Image.new("RGB", (400, 650), "#F2F2F2")
    draw = ImageDraw.Draw(img)

    # ---- Head ----
    draw.ellipse((170, 30, 230, 90), fill="#FFD6A5", outline="black")

    # ---- Inner Top ----
    draw.rectangle(
        (155, 110, 245, 260),
        fill=outfit["Top"]["color_code"],
        outline="black"
    )

    # ---- Outer Jacket (open front) ----
    if outfit["Outer"]["name"] != "None":
        color = outfit["Outer"]["color_code"]

        # Left side
        draw.rectangle((130, 100, 180, 270), fill=color, outline="black")
        # Right side
        draw.rectangle((220, 100, 270, 270), fill=color, outline="black")

        # Collar (simple triangles)
        draw.polygon([(130, 100), (180, 100), (155, 130)],
                     fill=color, outline="black")
        draw.polygon([(220, 100), (270, 100), (245, 130)],
                     fill=color, outline="black")

    # ---- Bottom ----
    draw.rectangle(
        (140, 260, 260, 420),
        fill=outfit["Bottom"]["color_code"],
        outline="black"
    )

    # ---- Legs ----
    draw.rectangle((150, 420, 185, 550),
                   fill=outfit["Bottom"]["color_code"], outline="black")
    draw.rectangle((215, 420, 250, 550),
                   fill=outfit["Bottom"]["color_code"], outline="black")

    # ---- Shoes ----
    draw.rectangle((145, 550, 190, 600),
                   fill=outfit["Shoes"]["color_code"], outline="black")
    draw.rectangle((210, 550, 255, 600),
                   fill=outfit["Shoes"]["color_code"], outline="black")

    draw.text((110, 610), "Outfit Preview (Layered)", fill="black")

    return img


# ======================
# UI
# ======================
st.title("👕 Outfit Generator")
st.write("Generate a random outfit with colors and a visual preview.")

if st.button("Generate Outfit"):
    outfit = generate_outfit()

    st.subheader("Outfit Details")
    for category, item in outfit.items():
        st.write(
            f"**{category}**: {item['name']} "
            f"(Color: {item['color_name']})"
        )

    st.subheader("Outfit Image")
    st.image(generate_outfit_image(outfit), use_container_width=True)

    st.success("Outfit generated successfully!")
