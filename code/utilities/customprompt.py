# flake8: noqa
from langchain.prompts import PromptTemplate

template = """{summaries}
Please reply to the question using only the information present in the text above. 
Include references to the sources you used to create the answer if those are relevant ("SOURCES"). 
If you can't find it, reply politely that the information is not in the knowledge base.
Question: {question}
Answer:"""

PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])

EXAMPLE_PROMPT = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)


extract_subs_template = """You are a counselor specializing in insurance products. When a 'Question' comes in, you can read the question and extract the subscription name and the subscription Date  from it and return it.
Please extract the date by the month. If you can't extract it, answer none.  Please read the examples below and answer the questions.

EXAMPLE
Question: 나는 92년에 교보손실의료보험에 가입했어
Answer: subscription Name: 교보손실의료보험 , subscription Date: 1992

END OF EXAMPLE

EXAMPLE
Question: 나는 교보손실의료보험을 1992년 6월에 가입했어
Answer: subscription Name: 교보손실의료보험, subscription Date: 1992.06

END OF EXAMPLE

EXAMPLE
Question: 안녕
Answer: subscription Name: none , subscription Date: none

END OF EXAMPLE

Question:{question}
Answer: 
"""

EXTRACT_SUB_PROMPT = PromptTemplate(template=extract_subs_template, input_variables=["question"])
