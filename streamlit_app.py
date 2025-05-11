import streamlit as st
import pandas as pd
import plotly.express as px
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Настройки страницы
st.set_page_config(page_title="AI-агент: Распределение задач", layout="wide")
st.title("🧠 AI-агент для распределения задач")
st.markdown("Вставьте список задач, и агент классифицирует их по Матрице Эйзенхауэра.")

# Ввод задач
tasks_input = st.text_area("Введите задачи (по одной на строку)", height=200)

# Ключ зашит напрямую
api_key = "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"

if st.button("📊 Классифицировать задачи") and tasks_input:
    prompt = PromptTemplate.from_template(
        "Ты эксперт по продуктивности. Пользователь отправит список задач. Раздели их по Матрице Эйзенхауэра на 4 категории:\n\n"
        "1. Важно и срочно\n2. Важно, но не срочно\n3. Неважно, но срочно\n4. Неважно и не срочно\n\n"
        "Верни таблицу в CSV-формате с колонками: Задача,Категория,Обоснование\n\n"
        "Список задач:\n{input}"
    )

    llm = ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name="openrouter/deepseek/deepseek-chat",
        temperature=0.3
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    with st.spinner("🤖 Обработка задач..."):
        result = chain.run(tasks_input)

    try:
        # Парсинг таблицы из CSV
        from io import StringIO
        df = pd.read_csv(StringIO(result))
        st.success("✅ Задачи успешно классифицированы!")

        # Таблица
        st.subheader("📋 Классифицированные задачи:")
        st.dataframe(df)

        # Визуализация: Матрица Эйзенхауэра
        coords = {
            "Важно и срочно": (0, 1),
            "Важно, но не срочно": (1, 1),
            "Неважно, но срочно": (0, 0),
            "Неважно и не срочно": (1, 0),
        }
        df["coords"] = df["Категория"].map(coords)
        df["X"] = df["coords"].apply(lambda x: x[0])
        df["Y"] = df["coords"].apply(lambda x: x[1])

        fig = px.scatter(
            df, x="X", y="Y", text="Задача",
            title="Матрица Эйзенхауэра",
            width=800, height=600
        )
        fig.update_traces(textposition="top center")
        fig.update_xaxes(showticklabels=False, title="")
        fig.update_yaxes(showticklabels=False, title="")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"❌ Ошибка при обработке результата:\n{e}")
