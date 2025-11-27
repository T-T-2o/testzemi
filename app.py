import streamlit as st

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

#テスト
"""
img = 
st.import(cv2)
"""

