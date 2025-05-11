import streamlit as st

st.title("AI Task Manager")

tasks = st.text_area("Введите список задач", height=200)

if st.button("Анализировать"):
    st.success("✅ Анализ задач выполнен!")
    st.write("Пока тут будет простой текст. Далее подключим ИИ и визуализацию.")
