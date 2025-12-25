import streamlit as st
import random
from PIL import Image, ImageDraw
import math

st.set_page_config(layout="wide")
st.title("Outfit Recommendation – Silhouette & Pattern Enhanced")

# =====================
# 1. User Input
# =====================

st.header("Basic Attributes")

gender = st.selectbox("Gender", ["Male", "Female"])
body_type = st.selectbox("Body Type", ["Slim", "Average", "Athletic", "Curvy", "Plus-size"])
has_hoodie = st.checkbox("Wear Hoodie (Outer)")
pattern_type = st.selectbox("Pattern", ["None", "Star Pattern"])

color_name = st.selectbox("Color", ["Black", "Navy", "Beige", "Green", "Red"])

COLOR_RGB = {
    "Black": (40, 40, 40),
    "Navy": (50, 70, 110),
    "Beige": (210, 200, 170),
    "Green": (70, 120, 90),
    "Red": (150, 60, 60)
}

# =====================
# 2. Silhouette Parameters
# =====================

GENDER_SHAPE = {
    "Male": {"shoulder": 1.2, "waist": 0.9, "hip": 0.95},
    "Female": {"shoulder": 0.9, "waist": 0.8, "hip": 1.2}
}

BODY_SCALE = {
    "Slim": 0.85,
    "Average": 1.0,
    "Athletic": 1.1,
    "Curvy": 1.15,
    "Plus-size": 1.3
}

# =====================
# 3. Drawing Utilities
# =====================

def draw_star(draw, cx, cy, r, color):
    points = []
    for i in range(10):
        angle = i * math.pi / 5
        radius = r if i % 2 == 0 else r / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=color)

def draw_pattern(draw, area, pattern, color):
    if pattern == "Star Pattern":
        x1, y1, x2, y2 = area
        for x in range(x1 + 15, x2, 40):
            for y in range(y1 + 20, y2, 40):
                draw_star(draw, x, y, 8, (255, 255, 255))

# =====================
# 4. Image Generator
# =====================

def generate_image():
    img = Image.new("RGB", (320, 520), "white")
    d = ImageDraw.Draw(img)

    base_color = COLOR_RGB[color_name]

    scale = BODY_SCALE[body_type]
    gender_shape = GENDER_SHAPE[gender]

    shoulder = 70 * gender_shape["shoulder"] * scale
    waist = 55 * gender_shape["waist"] * scale
    hip = 65 * gender_shape["hip"] * scale

    center = 160

    # Head
    d.ellipse((130, 20, 190, 80), fill=(220, 200, 180))

    # Torso polygon (real silhouette)
    torso = [
        (center - shoulder, 90),
        (center + shoulder, 90),
        (center + waist, 200),
        (center + hip, 320),
        (center - hip, 320),
        (center - waist, 200)
    ]
    d.polygon(torso, fill=base_color, outline="black")

    # Pattern
    draw_pattern(d, (center - hip, 90, center + hip, 320), pattern_type, base_color)

    # Hoodie (very visible)
    if has_hoodie:
        d.pieslice(
            (center - 55, 60, center + 55, 130),
            start=180,
            end=360,
            fill=base_color,
            outline="black",
            width=3
        )

    # Legs
    d.rectangle((center - 45, 320, center - 5, 470), fill=base_color)
    d.rectangle((center + 5, 320, center + 45, 470), fill=base_color)

    return img

# =====================
# 5. Output
# =====================

st.header("Generated Outfit (Improved Visuals)")

image = generate_image()
st.image(image)

st.subheader("Outfit Attributes")
st.json({
    "Gender": gender,
    "Body Type": body_type,
    "Hoodie": has_hoodie,
    "Pattern": pattern_type,
    "Color": color_name
})
