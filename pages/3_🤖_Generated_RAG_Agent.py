"""Streamlit page showing builder config."""
import streamlit as st
from typing import cast
from agent_utils import (
    RAGAgentBuilder,
    ParamCache
)
from constants import (
    AGENT_CACHE_DIR,
)

from streamlit_pills import pills


####################
#### STREAMLIT #####
####################



st.set_page_config(page_title="Generated RAG Agent", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Generated RAG Agent")
st.info(
    "This is generated by the builder in the above section.", icon="ℹ️"
)

if "agent_messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.agent_messages = [
        {"role": "assistant", "content": "Ask me a question!"}
    ]

def add_to_message_history(role, content):
    message = {"role": role, "content": str(content)}
    st.session_state.agent_messages.append(message) # Add response to message history

agent = None
if "selected_id" in st.session_state.keys():
    selected_id = st.session_state.selected_id
    if selected_id is not None:
        # load agent from agent cache
        cache = ParamCache.load_from_file(AGENT_CACHE_DIR / f"{selected_id}.json")
        if cache.agent is not None:
            agent = cache.agent
            for message in st.session_state.agent_messages: # Display the prior chat messages
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # don't process selected for now
            if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
                add_to_message_history("user", prompt)
                with st.chat_message("user"):
                    st.write(prompt)

            # If last message is not from assistant, generate a new response
            if st.session_state.agent_messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = agent.chat(prompt)
                        st.write(str(response))
                        add_to_message_history("assistant", response)
        else:
            st.info("Agent not created. Please create an agent in the above section.")
    else:
        st.info("Agent not created. Please create an agent in the above section.")
else:
    st.info("Agent not created. Please create an agent in the above section.")


# agent = None
# if "agent_builder" in st.session_state.keys():
#     agent_builder = cast(RAGAgentBuilder, st.session_state.agent_builder)
#     if agent_builder.cache.agent is not None:
#         agent = agent_builder.cache.agent
#         for message in st.session_state.agent_messages: # Display the prior chat messages
#             with st.chat_message(message["role"]):
#                 st.write(message["content"])

#         # don't process selected for now
#         if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
#             add_to_message_history("user", prompt)
#             with st.chat_message("user"):
#                 st.write(prompt)

#         # If last message is not from assistant, generate a new response
#         if st.session_state.agent_messages[-1]["role"] != "assistant":
#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     response = agent.chat(prompt)
#                     st.write(str(response))
#                     add_to_message_history("assistant", response)
#     else:
#         st.info("Agent not created. Please create an agent in the above section.")
# else:
#     st.info("Agent not created. Please create an agent in the above section.")
