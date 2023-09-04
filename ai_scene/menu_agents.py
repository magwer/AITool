import streamlit as st

from ai_scene.agent_data import AgentDataHelper


def display():
    def refresh():
        pass

    st.button("添加演员", type="primary", on_click=AgentDataHelper.create_agent)
    st.button("刷新", on_click=refresh)
    AgentDataHelper.create_agents_tab()
