import re
import streamlit as st
from streamlit_chat_kyobo import message
from utilities.openAI_helper import openAI_helper
from utilities.bing_helper import bing
import logging


st.set_page_config(layout="wide")
st.markdown("""
<style>
.welcome {
  display: block;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  border: 1px solid #90ee90;  /* 녹색 테두리 */
  background-color: #f0fff0;  /* 박스 내부의 연한 녹색 */
  padding: 10px;
  border-radius: 5px; /* 박스 모서리 둥글게 */
}

.introduction {
 font-family : "돋음";
  font-size: 15px;
}
#MainMenu {visibility: hidden;}

</style>

<div class="welcome">
    안녕하세요! <br>
    교보생명 임직원 업무활용을 위한 교보GPT입니다. <br>
    만나서 반갑습니다~☺
</div>
<br/>

""", unsafe_allow_html=True)

def clear_text_input():
    st.session_state['open_question'] = st.session_state['input']
    st.session_state['input'] = ""

def clear_chat_data():
    st.session_state['input'] = ""
    st.session_state['open_chat_history'] = [

            {"role": "system", "content": "You are a helpful and kind Korea AI Assistant. You must reply only in Korean"},
            ]

# Initialize chat history
if 'open_question' not in st.session_state:
    st.session_state['open_question'] = None
if 'open_chat_history' not in st.session_state:
    st.session_state['open_chat_history'] = [
            {"role": "system", "content": "You are a helpful and kind Korea AI Assistant. You must reply only in Korean"},
        ]
if 'source_documents' not in st.session_state:
    st.session_state['source_documents'] = []
openAI_Helper = openAI_helper()
bing = bing()

# load synonym data

clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)

st.session_state['input'] = st.chat_input(placeholder="type your open_question")
if st.session_state['input']:
    clear_text_input()

#clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)

if st.session_state['open_question']:
 # 빙서치
   # open_question, result = bing.bing_search(st.session_state['open_question'])
    open_question, result = openAI_Helper.get_chatgpt_answer(st.session_state['open_question'], st.session_state['open_chat_history'])
    st.session_state['open_chat_history'].append(open_question)
    st.session_state['open_chat_history'].append(result)
    # st.session_state['source_documents'].append(sources)
    st.session_state['open_question'] = []


if st.session_state['open_chat_history']:
    for i in range(1, len(st.session_state['open_chat_history'])):
        if st.session_state['open_chat_history'][i]['role'] == 'user':
            message(st.session_state['open_chat_history'][i]['content'], is_user=True, key=str(i) + 'openGpt_user')
        else:
            message(st.session_state['open_chat_history'][i]['content'], key=str(i)+'openGpt' )
      #  st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')


#clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)
