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

synonym_df = llm_helper.vector_store.get_synonym_results()

import re
sent = "안녕 command test 호호"
for idx, row in synonym_df.iterrows():
    sent = re.sub("|".join(row.synonymList), row.title, sent)

print(sent)


