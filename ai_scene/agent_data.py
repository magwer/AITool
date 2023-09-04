from typing import Optional

from langchain.schema import SystemMessage, BaseMessage
import streamlit as st

from ai_scene import llm_data


class AgentData(object):

    def __init__(self, uid: int):
        self.name: str = "New Agent"
        self.profile: str = ""
        self.avatar: str = "🐹"
        self.messages: list[BaseMessage] = list()
        self.uid = uid
        self.update_prompt()

    def update_prompt(self):
        sm = SystemMessage(
            content=st.session_state.agent_prompt.replace("{name}", self.name).replace("{profile}", self.profile)
        )
        if len(self.messages) == 0:
            self.messages.append(sm)
        else:
            self.messages[0] = sm

    def add_message(self, message: BaseMessage):
        self.messages.append(message)

    def delete_message(self, message: BaseMessage):
        for i, msg in enumerate(self.messages):
            if msg == message:
                self.messages.pop(i)
                break


class AgentDataHelper(object):

    @staticmethod
    def get_agents() -> list[AgentData]:
        if "agents" not in st.session_state:
            st.session_state["agents"] = list[AgentData]()
        return st.session_state.agents

    @staticmethod
    def create_agent():
        agents = AgentDataHelper.get_agents()
        agents.append(AgentData(len(agents)))

    @staticmethod
    def get_agent(name: str) -> Optional[AgentData]:
        for agent in AgentDataHelper.get_agents():
            if agent.name == name:
                return agent
        return None

    @staticmethod
    def remove_agent_by_name(name: str):
        agents = AgentDataHelper.get_agents()
        for i, agent in enumerate(agents):
            if agent.name == name:
                agents.pop(i)
                break

    @staticmethod
    def remove_agent(agent: AgentData):
        AgentDataHelper.get_agents().remove(agent)

    @staticmethod
    def add_agent_to_tab(agent: AgentData):
        name_input = st.text_input("Name", agent.name, key=("agname-" + str(agent.uid)))
        profile_input = st.text_area("Profile", agent.profile, key=("agprof-" + str(agent.uid)))
        avatar_input = st.text_input("Avatar", agent.avatar, key=("agava" + str(agent.uid)))
        agent.name = name_input
        agent.profile = profile_input
        agent.avatar = avatar_input
        agent.update_prompt()

        def del_agent():
            AgentDataHelper.remove_agent(agent)

        st.button("删除演员", on_click=del_agent, key=("agdel-" + str(agent.uid)))

    @staticmethod
    def create_agents_tab():
        agent_names: list[str] = []
        agents = AgentDataHelper.get_agents()
        for agent in agents:
            agent_names.append(agent.name + agent.avatar)

        if len(agent_names) > 0:
            for i, tab in enumerate(st.tabs(agent_names)):
                with tab:
                    AgentDataHelper.add_agent_to_tab(agents[i])
