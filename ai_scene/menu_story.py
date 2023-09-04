import asyncio
import threading
from typing import Optional, Any, Union, Coroutine
from uuid import UUID

import streamlit as st
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, LLMResult, BaseMessage, AIMessage, ChatGeneration
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx, ScriptRunContext

from ai_scene import llm_data
from ai_scene.message_history import MessageHistoryHelper, MessageHistory


class __LLMCallback(AsyncCallbackHandler):

    def __init__(self, agent_name: str, result_list: list[BaseMessage], index: int, context: ScriptRunContext):
        self.agent_name: str = agent_name
        self.result_list: list[BaseMessage] = result_list
        self.index: int = index
        self.context = context

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> None:
        generation = response.generations[0][0]
        if isinstance(generation, ChatGeneration) and isinstance(generation.message, AIMessage):
            self.on_result(generation.message)
        else:
            self.on_result(AIMessage(content="Unexpected generation type"))

    def on_llm_error(
            self,
            error: Union[Exception, KeyboardInterrupt],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> None:
        self.on_result(AIMessage(content=str(error)))

    def on_result(self, message: AIMessage):
        add_script_run_ctx(threading.current_thread(), self.context)
        ai_history = MessageHistory(self.agent_name, message)
        MessageHistoryHelper.add_history(ai_history)
        ai_history.write(len(MessageHistoryHelper.get_message_histories()) - 1)


async def __on_input(user_input: str, context: ScriptRunContext):
    add_script_run_ctx(threading.current_thread(), context)
    chat_model: ChatOpenAI = llm_data.get_llm()
    user_msg = HumanMessage(content=user_input)
    history = MessageHistory("user", user_msg)
    MessageHistoryHelper.add_history(history)
    history.write(len(MessageHistoryHelper.get_message_histories()) - 1)
    st.session_state.llm_async = len(history.targets)

    jobs = list[Coroutine[Any, Any, LLMResult]]()
    result_list = list[BaseMessage]()
    for i, target in enumerate(history.targets):
        result_list.append(AIMessage(content="Not Responded yet!"))
        job = chat_model.agenerate([target.messages], callbacks=[__LLMCallback(target.name, result_list, i, context)])
        jobs.append(job)

    for job in jobs:
        await job


def display():
    MessageHistoryHelper.write_histories()

    if "last_llm_input" not in st.session_state:
        st.session_state["last_llm_input"] = ""

    last_input = st.session_state.last_llm_input
    if last_input is not None and len(last_input) > 0:
        st.chat_input("演员酝酿情绪中~~", disabled=True)
        print("a: " + str(st))
        asyncio.run(__on_input(last_input, get_script_run_ctx()))
        st.session_state.last_llm_input = None
        st._rerun()
    else:
        userinput = st.chat_input("我是导演~~", disabled=False)
        if userinput is not None and len(userinput) > 0:
            st.session_state.last_llm_input = userinput
            st._rerun()
        else:
            st.session_state.last_llm_input = None
