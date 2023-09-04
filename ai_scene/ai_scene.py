import streamlit as st
from streamlit_option_menu import option_menu

from ai_scene import menu_serialize, menu_agents, menu_story, menu_settings, llm_data

st.image("./ai_scene/header.png")
selected = option_menu(None, ["演员列表", "情景演绎", "参数选项", "预设加载"], 0, None,
                       ["person-fill-gear", "camera-reels-fill", "gear-fill", "file-earmark-fill"],
                       "horizontal")

llm_data.init_llm()

if selected == "演员列表":
    menu_agents.display()
elif selected == "情景演绎":
    menu_story.display()
elif selected == "参数选项":
    menu_settings.display()
elif selected == "预设加载":
    menu_serialize.display()
