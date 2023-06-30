import re
import streamlit as st
from streamlit_chat import message
from utilities.helper import LLMHelper
import logging

def clear_text_input():
    st.session_state['question'] = st.session_state['input']
    st.session_state['input'] = ""

def clear_chat_data():
    st.session_state['input'] = ""
    st.session_state['source_documents'] = [] 


# Initialize chat history
if 'question' not in st.session_state:
    st.session_state['question'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [
            {"role": "system", "content": "You are a helpful and kind Korea AI Assistant. You must reply only in Korean"},
        ]
if 'source_documents' not in st.session_state:
    st.session_state['source_documents'] = []
llm_helper = LLMHelper()

# load synonym data


if st.session_state['question']:

    question, result = llm_helper.get_chatgpt_answer(st.session_state['question'], st.session_state['chat_history'])

    st.session_state['chat_history'].append(question)
    st.session_state['chat_history'].append(result)
    # st.session_state['source_documents'].append(sources)
    st.session_state['question'] = []
    message(str(st.session_state['chat_history']))

if st.session_state['chat_history']:
    for i in range(1, len(st.session_state['chat_history'])):
        if st.session_state['chat_history'][i]['role'] == 'user':
            message(st.session_state['chat_history'][i]['content'], is_user=True, key=str(i) + '_user')
        else:
            message(st.session_state['chat_history'][i]['content'], key=str(i))
      #  st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')

# Chat 
st.text_input("You: ", placeholder="type your question", key="input", on_change=clear_text_input)
clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)
