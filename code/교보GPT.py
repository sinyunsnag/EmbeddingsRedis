import re
import streamlit as st
from streamlit_chat_kyobo import message
from utilities.openAI_helper import openAI_helper
from utilities.bing_helper import bing
import logging
from openai.error import InvalidRequestError


st.set_page_config(layout="wide")
st.markdown("""
<style>
.welcome {
  color: black;
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
    만나서 반갑습니다~☺   베타버전으로 사용시 개선점은 이지모아에 요청부탁드립니다.
</div>
<br/>

""", unsafe_allow_html=True)


system_prompt = """
Please answer in Korean and write each question and choice in the questionnaire clearly and specifically. Keep your questions concise and make sure your options include a variety of options, considering all possible options.
Please write so that each question and option in the questionnaire can be distinguished by numbering them. This makes it easy for users to identify choices.
Put a blank line between each question in the questionnaire to improve readability. This allows users to have space to write down their answers to each question.
At the end of your form, add a free-filling section for users to fill out further. This allows users to provide detailed explanations or additional information on specific questions.
When filling out a questionnaire, it can be helpful to provide background information that users need to know in order to answer the questionnaire. For example, if your survey relates to a specific product or service, you can add a brief description of that product or service.
Kyobo Life Insurance Chairman Shin Chang-jae
For analysis, please derive detailed analysis results in an expert style.
Please make the report in the form of an expert report.
In the summary of the minutes, please provide a detailed summary of when, who, what, on what topics, and what conclusions were reached.
Please summarize the main points of the article.
Please list various options and examples in the questionnaire.
"""

def clear_text_input():
    st.session_state['open_question'] = st.session_state['input']
    st.session_state['input'] = ""

def clear_chat_data():
    st.session_state['input'] = ""
    st.session_state['open_chat_history'] = [

            {"role": "system", "content":  system_prompt },
            ]

# Initialize chat history
if 'open_question' not in st.session_state:
    st.session_state['open_question'] = None
if 'open_chat_history' not in st.session_state:
    st.session_state['open_chat_history'] = [
            {"role": "system", "content": system_prompt},
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
    try :
        open_question, result = openAI_Helper.get_chatgpt_answer(st.session_state['open_question'], st.session_state['open_chat_history'])

        st.session_state['open_chat_history'].append(open_question)
        st.session_state['open_chat_history'].append(result)
            # st.session_state['source_documents'].append(sources)
        st.session_state['open_question'] = []
    except InvalidRequestError:
        st.session_state['open_chat_history'] = [
            {"role": "system", "content":  system_prompt},
        ]
        #st.session_state['open_chat_history'].append("openAI 응답 token 4096 초과로 대화이력을 삭제하였습니다 다시 질문해주세요 ")
        message(st.session_state['open_question'], is_user=True )
        message("openAI 응답 token 16000 초과로 대화이력을 삭제하였습니다 다시 질문해주세요 " )
        
if st.session_state['open_chat_history']:
    for i in range(1, len(st.session_state['open_chat_history'])):
        if st.session_state['open_chat_history'][i]['role'] == 'user':
            message(st.session_state['open_chat_history'][i]['content'], is_user=True, key=str(i) + 'openGpt_user')
        else:
            message(st.session_state['open_chat_history'][i]['content'], key=str(i)+'openGpt' )
        #  st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')


#clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)
