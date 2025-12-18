import streamlit as st
"""
st.title("こんにちは、吉村ゼミ")

name = st.text_input("名前を入力してください")

st.write(name)

st.checkbox("同意します")
address = st.selectbox("次の中から現住所を教えてください",["大阪府","京都府","滋賀県"])
st.write(address)

hobby = st.multiselect("趣味を次から選択してください",["映画","読書","音楽","運動"])
st.write(hobby)

score = st.slider("この映画を10点満点で評価してください",0,10,0)
st.write(score)

st.radio("性別を選択してください",["男性","女性"])

list = [{"latitude":35.05, "longitude":135.76},#デフォルト現在地
        {"latitude":35.04, "longitude":135.75},#紫明小学校
       ]
st.map(list)

camera_photo = st.camera_input("写真を撮影します")
if camera_photo:
  st.image(camera, caption="写真", use_column_width=True)
"""
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

