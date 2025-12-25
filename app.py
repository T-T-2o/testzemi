def generate_image(outfit):
    base_color = COLOR_RGB[outfit["Color Theme"]]

    img = Image.new("RGB", (260, 440), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # Head
    d.ellipse([100, 20, 160, 80], fill=(220, 200, 180))

    # Outer (Jacket / Hoodie)
    d.rectangle([60, 100, 200, 260], fill=base_color, outline="black", width=3)

    # Hoodie hood
    if "Hoodie" in outfit["Outer"]:
        d.arc([80, 80, 180, 140], start=0, end=180, fill="black", width=4)

    # Inner (Tee / Shirt)
    inner_color = tuple(min(255, c + 40) for c in base_color)
    d.rectangle([80, 120, 180, 240], fill=inner_color, outline="black", width=2)

    # Graphic Tee logo
    if "Graphic Tee" in outfit["Inner"]:
        d.rectangle([110, 160, 150, 200], fill=(255, 255, 255))

    # Bottom
    bottom_color = tuple(max(0, c - 40) for c in base_color)
    d.rectangle([90, 260, 170, 400], fill=bottom_color, outline="black", width=3)

    return img
