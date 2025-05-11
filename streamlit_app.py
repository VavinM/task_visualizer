import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Task Manager", layout="centered")
st.title("🧠 AI Task Manager")

# Ввод задач
tasks = st.text_area("Введите список задач (по одной на строку):", height=200)

if st.button("Анализировать"):
    if not tasks.strip():
        st.warning("Пожалуйста, введите хотя бы одну задачу.")
        st.stop()

    # Промпт для модели
    prompt = f"""
Ты — эксперт по личной эффективности. Раздели задачи по Матрице Эйзенхауэра (4 квадранта):

1. Важно и срочно
2. Важно, но не срочно
3. Неважно, но срочно
4. Неважно и не срочно

Для каждой задачи верни:
- Название задачи
- Категорию
- Краткое обоснование

Формат вывода — таблица в Markdown.

Вот список задач:
{tasks}
"""

    # Прямо указываем ключ (небезопасно для публичных репозиториев!)
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat:free",
        "messages": [
            {"role": "system", "content": "Ты помощник по планированию задач."},
            {"role": "user", "content": prompt}
        ]
    }

    with st.spinner("🔍 Анализируем задачи..."):
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        st.markdown("### 🧩 Результат:")
        st.markdown(content)
    else:
        st.error("Ошибка при запросе к модели:")
        st.code(response.text)

