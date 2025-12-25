import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(layout="wide")
st.title("Outfit Visual Prototype (No AI Image)")

# --------------------
# User Inputs
# --------------------

gender = st.selectbox("Gender", ["Male", "Female"])
body_type = st.selectbox("Body Type", ["Slim", "Average", "Athletic", "Curvy", "Plus-size"])
pattern = st.selectbox("Pattern", ["Solid", "Striped", "Checked", "Graphic Print", "Minimal Logo"])
color = st.selectbox("Color", ["Black", "Navy", "Beige", "Green", "Red"])

COLOR_MAP = {
    "Black": (40, 40, 40),
    "Navy": (50, 70, 110),
    "Beige": (210, 200, 170),
    "Green": (70, 120, 90),
    "Red": (150, 60, 60)
}

# --------------------
# Silhouette Parameters
# --------------------

GENDER_PARAMS = {
    "Male": {"shoulder": 1.2, "hip": 0.9},
    "Female": {"shoulder": 0.9, "hip": 1.2}
}

BODY_PARAMS = {
    "Slim": 0.85,
    "Average": 1.0,
    "Athletic": 1.1,
    "Curvy": 1.15,
    "Plus-size": 1.3
}

# --------------------
# Pattern Drawing
# --------------------

def draw_pattern(draw, box, pattern, color):
    x1, y1, x2, y2 = box

    if pattern == "Solid":
        draw.rectangle(box, fill=color)

    elif pattern == "Striped":
        for x in range(x1, x2, 10):
            draw.rectangle((x, y1, x+5, y2), fill=color)

    elif pattern == "Checked":
        for x in range(x1, x2, 15):
            for y in range(y1, y2, 15):
                if (x + y) // 15 % 2 == 0:
                    draw.rectangle((x, y, x+15, y+15), fill=color)

    elif pattern == "Graphic Print":
        draw.rectangle(box, fill=color)
        draw.rectangle((x1+25, y1+30, x2-25, y1+80), fill="white")
        draw.text((x1+40, y1+40), "GRAPHIC", fill="black")

    elif pattern == "Minimal Logo":
        draw.rectangle(box, fill=color)
        draw.ellipse((x1+50, y1+40, x1+65, y1+55), fill="white")

# --------------------
# Image Generator
# --------------------

def generate_image():
    img = Image.new("RGB", (300, 500), "white")
    d = ImageDraw.Draw(img)

    base_width = 80
    base_hip = 70

    shoulder = base_width * GENDER_PARAMS[gender]["shoulder"] * BODY_PARAMS[body_type]
    hip = base_hip * GENDER_PARAMS[gender]["hip"] * BODY_PARAMS[body_type]

    center = 150

    # Head
    d.ellipse((125, 20, 175, 70), fill=(220, 200, 180))

    # Torso (Top)
    torso_box = (
        center - shoulder,
        80,
        center + shoulder,
        220
    )

    draw_pattern(d, torso_box, pattern, COLOR_MAP[color])

    # Bottom
    bottom_box = (
        center - hip,
        220,
        center + hip,
        420
    )

    d.rectangle(bottom_box, fill=COLOR_MAP[color])

    return img

# --------------------
# Output
# --------------------

st.header("Generated Outfit Image")

img = generate_image()
st.image(img)

st.subheader("Outfit Attributes")
st.write({
    "Gender": gender,
    "Body Type": body_type,
    "Pattern": pattern,
    "Color": color
})
