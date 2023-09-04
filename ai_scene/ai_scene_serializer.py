import os.path
import pickle

import streamlit as st

from ai_scene.agent_data import AgentDataHelper
from ai_scene.message_history import MessageHistoryHelper


class AISceneSerializer(object):

    @staticmethod
    def get_profile_path(profile: str) -> str:
        return "./ai_scene/profiles/" + profile

    @staticmethod
    def save_profile(profile: str):
        arr = [st.session_state.model, st.session_state.temperature, st.session_state.agent_prompt,
               AgentDataHelper.get_agents(), MessageHistoryHelper.get_message_histories()]

        with open(AISceneSerializer.get_profile_path(profile), "wb") as file:
            pickle.dump(arr, file)

    @staticmethod
    def load_profile(profile: str) -> bool:
        if not os.path.exists(AISceneSerializer.get_profile_path(profile)):
            return False
        with open(AISceneSerializer.get_profile_path(profile), "rb") as file:
            arr = pickle.load(file)
            st.session_state["model"] = arr[0]
            st.session_state["temperature"] = arr[1]
            st.session_state["agent_prompt"] = arr[2]
            st.session_state["agents"] = arr[3]
            st.session_state["messages"] = arr[4]
            return True
