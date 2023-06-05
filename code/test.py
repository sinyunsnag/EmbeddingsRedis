import streamlit as st
import os
import traceback
from utilities.helper import LLMHelper

llm_helper = LLMHelper()


llm_helper.vector_store.add_synonym_result(
    "커맨드 테스트",
    writer="원준호",
    regdate="20230605",
    title="커맨드 테스트",
    synonymList=["command test", "커맨드 태스트"]
)

print(llm_helper.vector_store.get_synonym_results())


