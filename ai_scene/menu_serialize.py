import streamlit as st

from ai_scene.ai_scene_serializer import AISceneSerializer


def display():
    if "profile_input" not in st.session_state:
        st.session_state["profile_input"] = ""
    st.session_state.profile_input = st.text_input("预设名称", st.session_state.profile_input)

    def load():
        if len(st.session_state.profile_input) > 0:
            if AISceneSerializer.load_profile(st.session_state.profile_input):
                st.session_state["last_serialize_status"] = "读取成功！"
            else:
                st.session_state["last_serialize_status"] = "文件不存在！"
        else:
            st.session_state["last_serialize_status"] = ""

    def save():
        if len(st.session_state.profile_input) > 0:
            AISceneSerializer.save_profile(st.session_state.profile_input)
            st.session_state["last_serialize_status"] = "写入成功！"
        else:
            st.session_state["last_serialize_status"] = ""

    col1, col2 = st.columns(2)

    clicked = False
    with col1:
        clicked = st.button("读取", type="primary", use_container_width=True, on_click=load) or clicked
    with col2:
        clicked = st.button("写入", type="secondary", use_container_width=True, on_click=save) or clicked
    if clicked:
        st.write(st.session_state.last_serialize_status)
