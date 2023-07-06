import re
import streamlit as st
from streamlit_chat import message
from utilities.helper import LLMHelper
from datetime import datetime
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

#화면구성
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
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>

<div class="welcome">
    <h3>교보생명의 보험약관을 설명해 드리는 교보 ChatGPT 입니다.</h3>
</div>
<div class="introduction">
<ol>
    <li>보다 정확한 내용을 파악하기 위해서 궁금하신 <b>보험명</b>을 포함하여 질문해주세요</li>
    <li>보험 가입하신 고객이라면 <b>가입날짜</b>까지 알려주시면 더욱 더 정확한 답변을 할 수가 있습니다.(날짜를 모르시면 최신약관으로 설명됩니다.)</li>
</ol>
</div>
""", unsafe_allow_html=True)

subscription_info = dict()

def fill_session_var(subscription_info):
    
    for info in subscription_info:
        if subscription_info[info] == "none":
            if st.session_state[info] == "":
                st.session_state[info] = ""
        else:
            st.session_state[info] = subscription_info[info]

def validation_check_subscription_info(subscription_info):
    
    not_enough_info = []

    for info in subscription_info:
        
        if info == "subscription_name":
            if subscription_info[info] == 'none':
                not_enough_info.append(info)

        elif info == "subscription_date":
            if subscription_info[info] and subscription_info[info] != 'none':
                now = datetime.now()
                if "YYYY" in subscription_info[info]:
                    subscription_info[info] = subscription_info[info].replace("YYYY", now.strftime('%Y'))
                elif "XXXX" in subscription_info[info]:
                    one_year_ago = now - relativedelta(years=1)
                    subscription_info[info] = subscription_info[info].replace("XXXX", one_year_ago.strftime('%Y'))
                elif "ZZZZ" in subscription_info[info]:
                    two_year_ago = now - relativedelta(years=2)
                    subscription_info[info] = subscription_info[info].replace("ZZZZ", two_year_ago.strftime('%Y'))                    
                
                    subscription_info[info] = re.sub(r'[^0-9]', '',  subscription_info[info])

                if len(subscription_info[info]) == 4 :
                    subscription_info[info] = subscription_info[info] +'01'
                    datetime.strptime(subscription_info[info], '%Y%m')
                
                if len(subscription_info[info]) != 6:
                    not_enough_info.append(info)

            elif subscription_info[info] == 'none':
                now = datetime.now()
                subscription_info[info] = now.strftime('%Y%m')
            
            else:
                not_enough_info.append(info)

        elif info == "intent":
            if subscription_info[info] == 'none':   
                not_enough_info.append(info)

        elif info == "sentence":
            if subscription_info[info] == 'none': 
                not_enough_info.append(info)

    return not_enough_info

def clear_text_input():
    st.session_state['question'] = chage_synonym(st.session_state['input'])
    st.session_state['question'] = st.session_state['input']
    st.session_state['input'] = ""    

    question, subscription_info = llm_helper.get_sentence_components(st.session_state['question'])
            
    st.session_state['not_enought_info_list'] = validation_check_subscription_info(subscription_info)

    fill_session_var(subscription_info)

    logging.info(f"***** st.session_state['not_enought_info_list'] : {st.session_state['not_enought_info_list']}")
    logging.info(f"***** st.session_state['subscription_name'] : {st.session_state['subscription_name']}")
    logging.info(f"***** st.session_state['subscription_date'] : {st.session_state['subscription_date']}")
    logging.info(f"***** st.session_state['intent'] : {st.session_state['intent']}")
    logging.info(f"***** st.session_state['sentence'] : {st.session_state['sentence']}")


def clear_chat_data():
    st.session_state['input'] = ""
    st.session_state['chat_history'] = []
    st.session_state['source_documents'] = []  
    st.session_state['subscription_history'] = []  
    

def make_chat_for_enought_info():

    chat_result = ""

    for val in st.session_state['not_enought_info_list']:

        if val == 'subscription_name':
            chat_result += " [보험 상품명] "
        elif val == 'subscription_date':
            chat_result += " [보험 가입일자] " 
        elif val == 'sentence':
            chat_result += " [보험 관련 궁금한점] "
    
    chat_result = "고객님," + chat_result + "을 포함해서 질문해주세요."        

    return chat_result

def chage_synonym(question):
    for idx, row in synonym_df.iterrows():
        question = re.sub("|".join(row.synonymList), row.title, question)
    return question   

       
llm_helper = LLMHelper()

# load synonym data
synonym_df = llm_helper.vector_store.get_synonym_results()


# Initialize chat history
if 'question' not in st.session_state:
    st.session_state['question'] = []

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'source_documents' not in st.session_state:
    st.session_state['source_documents'] = []

# if 'subscription_question' not in st.session_state:
#     st.session_state['subscription_question'] = []
#     st.session_state['year'] = ""
#     st.session_state['name'] = ""

if 'subscription_history' not in st.session_state:
    st.session_state['subscription_history']  = []

if 'not_enought_info_list' not in st.session_state:
    st.session_state['not_enought_info_list'] = []

if 'subscription_name' not in st.session_state:
    st.session_state['subscription_name'] = ""

if 'subscription_date' not in st.session_state:
    st.session_state['subscription_date'] = ""  

if 'intent' not in st.session_state:
    st.session_state['intent'] = ""

if 'sentence' not in st.session_state:
    st.session_state['sentence'] = ""    

# if 'not_enough_info_history' not in st.session_state:
#     st.session_state['not_enough_info_history'] = ""

logging.info(f"len(st.session_state['not_enought_info_list']) : {len(st.session_state['not_enought_info_list'])}")

if st.session_state['question'] and len(st.session_state['not_enought_info_list']) == 0:

    def get_hashkey_insurance_date(insurance_name, insurance_date):
        similar_insurance = llm_helper.vector_store.similarity_search_with_score_insurance(insurance_name, "*", index_name="insurance-index", k=4)
        best_insurance = similar_insurance.docs[0]
        
        date_list = [str(i) for i in ast.literal_eval(best_insurance.date)]
        date_list.append("현재")
        
        candidate_date = []
        for idx in range(1, len(date_list)):
            candidate_date.append((date_list[idx-1], date_list[idx]))

        insurance_key = best_insurance.insurance
        date_key = None
        for start, end in candidate_date:
            if start <= insurance_date < end:
                date_key = start
                sell_date = (start, end)
        
        if date_key is None:
            date_key = candidate_date[-1][0]
            sell_date = candidate_date[-1]

        candidate_date = date_list[:-1]

        search_key = insurance_key + ":" + date_key
        hash_key = hashlib.sha1(search_key.encode('utf-8')).hexdigest()    

        candidate_insurance = [ins.insurance for ins in similar_insurance.docs[1:]]
                
        return hash_key, insurance_key, sell_date, candidate_date, candidate_insurance

    import ast
    import hashlib
    
    hash_key, insurance_key, sell_date, candidate_date, candidate_insurance = get_hashkey_insurance_date(st.session_state['subscription_name'], st.session_state['subscription_date'])

    def _sell_date(dates):
        from dateutil.parser import parse

        start = parse(dates[0]).strftime("%Y년 %m월 %d일")

        if dates[1].isdigit():
            end = parse(dates[1]).strftime("%Y년 %m월 %d일")
        else:
            end = dates[1]
        return start + " ~ " + end

    sell_date = _sell_date(sell_date)

    intro = f"현재 답변은 <{sell_date}> 까지 판매된 <{insurance_key}> 약관 기준으로 설명할게요. \n\n"
    outro = "\n\n상세한 내용은 상품설명서를 반드시 확인해보시기 바랍니다."

    def _revised_date(dates):
        from dateutil.parser import parse
        dates = [parse(date).strftime("%Y년 %m월 %d일") for date in dates]
        return    ", ".join(dates)
    def _candidate_insurance(insurances):
        return ", ".join(insurances)

    candidate_date = _revised_date(candidate_date)
    candidate_insurance = _candidate_insurance(candidate_insurance)

    candidate_info = f"""\n\n
                        입력하신 정보와 유사한 보험 상품은 : {candidate_insurance} 가 있습니다."""
    
    question, result, _, sources = llm_helper.get_semantic_answer_lang_chain(st.session_state['question'], "", hash_key)

    result = intro + result + outro + candidate_info

    st.session_state['chat_history'].append((question, result))
    st.session_state['source_documents'].append(sources)
    st.session_state['question'] = []

elif len(st.session_state['not_enought_info_list']) > 0:
    st.session_state['chat_history'].append((st.session_state['question'], make_chat_for_enought_info()))
    st.session_state['question'] = []


if st.session_state['subscription_history']:
    for i in range(0, len(st.session_state['subscription_history']),1  ):
        if st.session_state['subscription_history'][i][0] : message(st.session_state['subscription_history'][i][0], is_user=True, key='sub' +str(i) + '_user')
        if st.session_state['subscription_history'][i][1] : message(st.session_state['subscription_history'][i][1], key= 'sub'+str(i))
    
if st.session_state['chat_history']:
    for i in  range(0, len(st.session_state['chat_history']), 1):
        if st.session_state['chat_history'][i][0] : message(st.session_state['chat_history'][i][0], is_user=True, key= str(i) + '_user')
        if st.session_state['chat_history'][i][1] : message(st.session_state['chat_history'][i][1], key=str(i))

 
# Chat 
st.text_input("You: ", placeholder="보험관련 질문을 해주세요(보험상품명과 가입날짜를 포함하면 좋습니다)", key="input", on_change=clear_text_input)
clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)
 
 
  #채팅창 아래로 바꾸고 표출순서 변경
  #   for i in range(0, 1, len(st.session_state['chat_history'])):
   #     message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')
    #    message(st.session_state['chat_history'][i][1], key=str(i))
    