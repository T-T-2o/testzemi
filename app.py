import streamlit as st

st.title("こんにちは、吉村ゼミ")

name = st.text_input("名前を入力してください")

st.write(name)

st.checkbox("同意します")
address = st.selectbox("次の中から現住所を教えてください",["大阪府","京都府","滋賀県"])

camera_photo = st.camera.input("写真を撮影します")
if camera_photo:
  st.image(camera, caption="写真", use_column_width=True)
