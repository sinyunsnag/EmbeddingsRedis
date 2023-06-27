import streamlit as st
import os
from utilities.helper import LLMHelper
import numpy as np
from collections import defaultdict
llm_helper = LLMHelper()




# llm_helper.vector_store.add_insurance_info("junho", "201204")


import ast
from datetime import datetime
from urllib.parse import quote, unquote

insurance_name = '실손보험'
date = '199905'

similar_insurance = llm_helper.vector_store.similarity_search_with_score_insurance(quote(insurance_name), "*", index_name="insurance-index", k=4)
best_insurance = similar_insurance.docs[0]


sell_date = []
date_list = [str(i) for i in ast.literal_eval(best_insurance.date)]
date_list.append("현재")

# 유사도로 검색한 보험을 해당 날짜에 팔지 않았따면?

for idx in range(1, len(date_list)):
    sell_date.append((date_list[idx-1], date_list[idx]))

date_key = None
for start, end in sell_date:
    if start <= date < end:
        print(start + " ~ " + end)
        date_key = start

if date_key is None:
    date_key = sell_date[-1][0]

print("입력된 보험 : ", insurance_name)

print("가장 유사한 보험 : ", unquote(best_insurance.insurance))

print("key : ", date_key)

print("팔던 날짜 : ", sell_date)

candidate_insurance = [unquote(ins.insurance) for ins in similar_insurance.docs[1:]]

print("유사한 보험 : ", candidate_insurance)

exit()

# 11111111111111111111111111111111111111111111
# 보험명 들어오면, 가장 유사한 보험명 뽑아내고?? 년도는?


# insurance:8546e2663fa3cd3f0e0ddf2c30de19a0be538470:20210331
insurance_name = '(무)교보실손의료비보험(갱신형)3'
similar_insurance = llm_helper.vector_store.similarity_search_with_score_insurance(insurance_name, "*", index_name="insurance-index", k=10)


insurance_dict = defaultdict(list)

for insurance in similar_insurance.docs:
    insurance.id
    print(insurance.insurance)
    insurance_dict[insurance.insurance].append(insurance.date)

print(insurance_dict)
exit()

# 2222222222222222222222222222222222222222
# 질문 들어오면, 임베딩 벡터들과 비교해 4개의 본문 찾아내는 부분.
# "*"부분에 hash(상품명:일자) 값을 넣으면 검색됨.
# result = llm_helper.vector_store.similarity_search("요실금 얼마야",  "f6707e308f4e88764ed7404a2a42964e80a8d01c", k=1000)
# # doc:embeddings:f6707e308f4e88764ed7404a2a42964e80a8d01c:17
# print(len(result))

exit()


# 33333333333333333333333333333333333333333333333333
# similarity search 할때, query 테스트 부분.
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Tuple
from redis.commands.search.query import Query

embedding = llm_helper.vector_store.embedding_function("요실금 얼마야")

# Prepare the Query
return_fields = ["metadata", "content", "vector_score"]
vector_field = "content_vector"
hybrid_fields = "f6707e308f4e88764ed7404a2a42964e80a8d01c"
# f6707e308f4e88764ed7404a2a42964e80a8d01c
base_query = (
    f"{hybrid_fields}=>[KNN 1000 @{vector_field} $vector AS vector_score]"
    # f"{hybrid_fields}=>[KNN {k} @{vector_field} $vector AS vector_score]"
)
redis_query = (
    Query(base_query)
    .return_fields(*return_fields)
    .sort_by("vector_score")
    # .paging(0, k)
    .dialect(2)
)
params_dict: Mapping[str, str] = {
    "vector": np.array(embedding)  # type: ignore
    .astype(dtype=np.float32)
    .tobytes()
}

# perform vector search
results = llm_helper.vector_store.client.ft("embeddings").search(redis_query, params_dict)
# doc:embeddings:f6707e308f4e88764ed7404a2a42964e80a8d01c:111

print(results.total)

# print(llm_helper.vector_store.get_insurance_info())

exit()