import re
import streamlit as st
from streamlit_chat import message
from utilities.helper import LLMHelper
from datetime import datetime
import logging

llm_helper = LLMHelper()

subscription_question = "23년이었나 그때였고 종신보험이야"
subscription_question = "종신보험인데 사망보험금이 얼마지"
subscription_question = "건강관리보험인데 병원비 돌려받을수 있나? 21년도쯤 가입했음"
subscription_question = "치매보험인데 중증치매 진단은 언제받는지 궁금해"
subscription_question = "무슨말인지? 보험 언제가입했는지 모르겠어"
subscription_question = "실손가입했는데 족저근막염 보상돼?"
subscription_question = "보험 가입은 했는데 언제인지 모르겠다 사고나서 보장금액 얼마 받는지 알고싶은데"



question, subscription_info = llm_helper.get_sentence_components(subscription_question)

logging.info(f"########## question : {question}")
logging.info(f"########## subscription_info : {subscription_info}")


