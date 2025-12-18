import streamlit as st

import random

# 服の候補リスト
tops = [
    "白Tシャツ", "黒Tシャツ", "シャツ", "パーカー", "ニット", "ジャケット"
]

bottoms = [
    "デニムパンツ", "黒スラックス", "チノパン", "ショートパンツ"
]

outerwear = [
    "なし", "カーディガン", "コート", "ダウンジャケット"
]

shoes = [
    "スニーカー", "革靴", "ローファー", "ブーツ", "サンダル"
]

accessories = [
    "なし", "腕時計", "ネックレス", "キャップ", "バックパック"
]

def generate_outfit():
    outfit = {
        "トップス": random.choice(tops),
        "ボトムス": random.choice(bottoms),
        "アウター": random.choice(outerwear),
        "靴": random.choice(shoes),
        "アクセサリー": random.choice(accessories)
    }
    return outfit

# 実行
if __name__ == "__main__":
    outfit = generate_outfit()
    print("🎽 今日のランダムコーデ 🎽")
    for key, value in outfit.items():
        print(f"{key}：{value}")


#テスト
"""
st.import(cv2)
img = cv2.imread("eiga.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()
"""

