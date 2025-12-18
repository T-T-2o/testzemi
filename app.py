import streamlit as st
import random
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="ランダム服装ジェネレーター", page_icon="👕")

# ----------------------
# 服データ
# ----------------------
tops = ["白Tシャツ", "黒Tシャツ", "シャツ", "パーカー", "ニット", "ジャケット"]
bottoms = ["デニムパンツ", "黒スラックス", "チノパン", "ショートパンツ"]
outerwear = ["なし", "カーディガン", "コート", "ダウンジャケット"]
shoes = ["スニーカー", "革靴", "ローファー", "ブーツ", "サンダル"]
accessories = ["なし", "腕時計", "ネックレス", "キャップ", "バックパック"]

# ----------------------
# コーデ生成
# ----------------------
def generate_outfit(season):
    if season == "夏":
        tops_season = ["白Tシャツ", "黒Tシャツ", "半袖シャツ"]
        outer = ["なし"]
    elif season == "冬":
        tops_season = ["ニット", "パーカー"]
        outer = ["コート", "ダウンジャケット"]
    elif season in ["春", "秋"]:
        tops_season = ["シャツ", "パーカー", "ジャケット"]
        outer = ["カーディガン", "ジャケット"]
    else:
        tops_season = tops
        outer = outerwear

    return {
        "トップス": random.choice(tops_season),
        "ボトムス": random.choice(bottoms),
        "アウター": random.choice(outer),
        "靴": random.choice(shoes),
        "アクセサリー": random.choice(accessories)
    }

# ----------------------
# 画像生成
# ----------------------
def generate_outfit_image(outfit):
    img = Image.new("RGB", (500, 600), "#F8F8F8")
    draw = ImageDraw.Draw(img)

    # タイトル
    draw.text((140, 30), "Today's Outfit", fill="black")

    y = 120
    for key, value in outfit.items():
        draw.rectangle((80, y - 10, 420, y + 40), outline="black", width=2)
        draw.text((100, y), f"{key}：{value}", fill="black")
        y += 80

    return img

# ----------------------
# Streamlit UI
# ----------------------
st.title("👕 ランダム服装ジェネレーター")
st.write("ボタンを押すと、コーデとその画像を生成します。")

season = st.selectbox("季節を選択してください", ["指定なし", "春", "夏", "秋", "冬"])

if st.button("コーデを生成する"):
    outfit = generate_outfit(season)

    st.subheader("🎽 今日のコーデ（テキスト）")
    for k, v in outfit.items():
        st.write(f"**{k}**：{v}")

    # 画像生成・表示
    outfit_image = generate_outfit_image(outfit)
    st.subheader("🖼️ コーデ画像")
    st.image(outfit_image, use_container_width=True)

    st.success("コーデと画像を生成しました！")
