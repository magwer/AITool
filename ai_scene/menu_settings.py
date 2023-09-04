import streamlit as st


def display():
    st.session_state.openai_base = st.text_area(
        "OpenAI Base", st.session_state.openai_base
    )

    st.session_state.openai_key = st.text_area(
        "OpenAI Key", st.session_state.openai_key
    )
    st.session_state.model = st.selectbox(
        "GPT Model",
        ("gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-4")
    )

    st.session_state.temperature = st.slider(
        "Temperature", 0.0, 1.0, 1.0, 0.05
    )

    st.session_state.agent_prompt = st.text_area(
        "演员 Prompt 模板", st.session_state.agent_prompt
    )
