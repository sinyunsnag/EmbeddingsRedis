import re
import streamlit as st
from streamlit_chat import message
from utilities.helper import LLMHelper
from datetime import datetime


subscription_info = dict()
def clear_text_input():
  #  st.session_state['question'] = chage_synonym(st.session_state['input'])
    if chk_subscription_info(subscription_info):
        st.session_state['question'] = st.session_state['input']
        st.session_state['input'] = ""
    else :
        st.session_state['subscription_question'] = st.session_state['input']    
        st.session_state['input'] = ""

def clear_chat_data():
    st.session_state['input'] = ""
    st.session_state['chat_history'] = []
    st.session_state['source_documents'] = []  
    st.session_state['subscription_history'] = []  

def chage_synonym(question):
    print("테스트 테스트으")
    for idx, row in synonym_df.iterrows():
        question = re.sub("|".join(row.synonymList), row.title, question)
    return question   


# 데이터 유효성 검사
def chk_subscription_info(subscription_info):
    if not subscription_info.get('subscriptionName') or len(subscription_info.get('subscriptionName')) < 5 :
        return False
    elif not subscription_info.get('subscriptionDate') or subscription_info.get('subscriptionDate') =='none' :
        now = datetime.now()
        subscription_info['subscriptionDate'] = now.strftime('%Y%m')
        return True
    # 년도만 있을 경우 1월을 더해줌
    elif subscription_info.get('subscriptionDate') :
        if len(subscription_info.get('subscriptionDate')) == 4 :
            subscription_info['subscriptionDate'] = subscription_info['subscriptionDate'] +'01'
        try:
            subscription_info['subscriptionDate'] = re.sub(r'[^0-9]', '',  subscription_info['subscriptionDate'])
            datetime.strptime(subscription_info['subscriptionDate'], '%Y%m')
        except ValueError:
            print("날짜형식에러")
            return False
        return True
    else: 
        return True
    
 
        
llm_helper = LLMHelper()

# load synonym data
#synonym_df = llm_helper.vector_store.get_synonym_results()

# Chat 
st.text_input("You: ", placeholder="type your question", key="input", on_change=clear_text_input)
clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)


# Initialize chat history
if 'question' not in st.session_state:
    st.session_state['question'] = []
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'source_documents' not in st.session_state:
    st.session_state['source_documents'] = []
if 'subscription_question' not in st.session_state:
    st.session_state['subscription_question'] = []
    st.session_state['year'] = ""
    st.session_state['name'] = ""
if 'subscription_history' not in st.session_state:
    st.session_state['subscription_history']  = []
    st.session_state['subscription_history'].append(("", "가입하신 상품명과 가입년도를 입력해주세요 예: 1992년에 가입했고 상품명은? "))
#값 초기화
# chatHistory에 질문이 추가되면 꼬일수가 있어서 history에 추가 안하고 message로 표출해야 됌
if st.session_state['subscription_question']:
    question, subscription_info = llm_helper.get_extract_entity(st.session_state['subscription_question'])
   # st.session_state['chat_history'].append((question, result))
    if(chk_subscription_info(subscription_info)):
        st.session_state['subscription_history'].append((st.session_state['subscription_question'] ,"상품명과 가입년도가 인식되었습니다.{0} {1} ".format(subscription_info['subscriptionDate'] ,subscription_info['subscriptionName'] ) )  )
        st.session_state['subscription_question'] = []
        st.session_state['name'] =subscription_info['subscriptionName']
        st.session_state['date'] =subscription_info['subscriptionDate']
    else :
        st.session_state['subscription_history'].append(( st.session_state['subscription_question'] ,"죄송하지만 보험상품명과 년도를 입력해주셔야 정확한 답변이 가능합니다." )  )
if st.session_state['question']:
    question, result, _, sources = llm_helper.get_semantic_answer_lang_chain(st.session_state['question'], st.session_state['chat_history'])
    st.session_state['chat_history'].append((question, result))
    st.session_state['source_documents'].append(sources)

if st.session_state['chat_history']:
    for i in range(len(st.session_state['chat_history'])-1, -1, -1):
        message(st.session_state['chat_history'][i][1], key=str(i))
      #  st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')
        message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')


if st.session_state['subscription_history']:
    for i in range(len(st.session_state['subscription_history'])-1, 0, -1):
        message(st.session_state['subscription_history'][i][1], key= 'his'+str(i))
        message(st.session_state['subscription_history'][i][0], is_user=True, key= 'his'+str(i) + '_user')
    message(st.session_state['subscription_history'][0][1], key='his')

 
  #채팅창 아래로 바꾸고 표출순서 변경
  #   for i in range(0, 1, len(st.session_state['chat_history'])):
   #     message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')
    #    message(st.session_state['chat_history'][i][1], key=str(i))
       