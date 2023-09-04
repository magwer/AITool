from typing import Optional

import streamlit as st
from langchain.schema import BaseMessage, HumanMessage

from ai_scene.agent_data import AgentData, AgentDataHelper


class MessageHistory(object):

    def __init__(self, speaker: str, message: BaseMessage):
        self.speaker: str = speaker
        self.message: BaseMessage = message
        self.targets: list[AgentData] = self.__get_targets()
        for target in self.targets:
            target.add_message(message)
        self.deleted = False

    def __get_targets(self) -> list[AgentData]:
        agents = AgentDataHelper.get_agents()
        result_agents = []
        if type(self.message) == HumanMessage:
            for line in self.message.content.split('\n'):
                if line.startswith("@all "):
                    return agents
                for agent in agents:
                    if line.find("@" + agent.name) >= 0:
                        result_agents.append(agent)

        return result_agents

    def delete(self):
        self.deleted = True
        if self.speaker == "user":
            for target in self.targets:
                target.delete_message(self.message)
        else:
            agent = AgentDataHelper.get_agent(self.speaker)
            if agent is not None:
                agent.delete_message(self.message)

    def write(self, index: int):
        if self.speaker == "user":
            with st.chat_message("user"):
                content: str = self.message.content
                for line in content.split('\n'):
                    if line.startswith("@"):
                        try:
                            space_index = line.index(" ")
                            st.markdown("**" + line[0:space_index] + "**" + line[space_index:])
                        except ValueError:
                            st.write(line)
                    else:
                        st.write(line)
                if not self.deleted:
                    st.button("屏蔽", on_click=self.delete, key="block_" + str(index))
                else:
                    st.button("已屏蔽", key="unblock_" + str(index))
        else:
            avatar: Optional[str] = None
            agent = AgentDataHelper.get_agent(self.speaker)
            if agent is not None:
                avatar = agent.avatar
            with st.chat_message("assistant", avatar=avatar):
                st.write(self.message.content)
                if not self.deleted:
                    st.button("屏蔽", on_click=self.delete, key="block_" + str(index))
                else:
                    st.button("已屏蔽", key="unblock_" + str(index))


class MessageHistoryHelper(object):

    @staticmethod
    def get_message_histories() -> list[MessageHistory]:
        if "messages" not in st.session_state:
            st.session_state["messages"] = list[MessageHistory]()
        return st.session_state.messages

    @staticmethod
    def add_history(history: MessageHistory):
        MessageHistoryHelper.get_message_histories().append(history)

    @staticmethod
    def write_histories():
        for i, history in enumerate(MessageHistoryHelper.get_message_histories()):
            history.write(i)
