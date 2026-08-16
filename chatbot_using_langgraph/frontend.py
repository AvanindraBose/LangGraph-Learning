import streamlit as st
import uuid
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# ********************************************* Utility Function ************************************

def generate_thread_id():
    thread_id = uuid.uuid4()

    return thread_id

def reset_chat() :
    #  generate a new thread_id
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id) :
    if thread_id not in st.session_state['chat_threads'] :
        st.session_state['chat_threads'].append(thread_id)


# session_state is a dictionary which is used to persist the memeory of frontend.
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

# ***************************************** Sidebar ******************************************

st.sidebar.title('Lang Graph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Converstaions')

for thread_id in st.session_state['chat_threads'] :
    st.sidebar.button(str(thread_id))

# ******************************************* Main UI ***************************************

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type Here !!")

if user_input :

    st.session_state['message_history'].append({'role':'user' , 'content' : user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {'configurable' : {'thread_id' : st.session_state['thread_id']}}
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