import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# session_state is a dictionary which is used to persist the memeory of frontend.
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

CONFIG = {'configurable' : {'thread_id' : "1"}}

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type Here !!")

if user_input :

    st.session_state['message_history'].append({'role':'user' , 'content' : user_input})
    with st.chat_message('user'):
        st.text(user_input)


    with st.chat_message('assistant'):
        #  Implementing Streaming Using LLM

        ai_response = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages' : HumanMessage(content=user_input)},
                CONFIG,
                stream_mode="messages"
            )
        )
    st.session_state['message_history'].append({'role':'assistant' , 'content' : ai_response})