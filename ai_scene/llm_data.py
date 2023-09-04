import streamlit as st
from langchain.chat_models import ChatOpenAI


def init_llm():
    if "openai_base" not in st.session_state:
        st.session_state["openai_base"] = ""
    if "openai_key" not in st.session_state:
        st.session_state["openai_key"] = ""
    if "model" not in st.session_state:
        st.session_state["model"] = "gpt-3.5-turbo"
    if "temperature" not in st.session_state:
        st.session_state["temperature"] = 1.0
    if "agent_prompt" not in st.session_state:
        st.session_state["agent_prompt"] = open("./ai_scene/ai_scene_agent_prompt.txt", "r", encoding="utf-8").read()


def get_llm() -> ChatOpenAI:
    init_llm()
    return ChatOpenAI(temperature=st.session_state.temperature, model=st.session_state.model,
                      openai_api_key=st.session_state.openai_key, openai_api_base=st.session_state.openai_base)
