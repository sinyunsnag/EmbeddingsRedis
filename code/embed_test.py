import streamlit as st
import os
from utilities.helper import LLMHelper
import numpy as np
from collections import defaultdict
llm_helper = LLMHelper()



# 0000000000000000000000000000000000000
# 여러 text similarity 모델이 있따.
# 모델 차원이 1000, 1500, 4000 << 비교해봐도 좋을듯.

# from numpy import dot
# from numpy.linalg import norm
# import numpy as np

# # 코사인 유사도 함수 
# def cos_sim(A, B):
#        return dot(A, B)/(norm(A)*norm(B))

# eng = "text-embedding-ada-002"
# res = llm_helper.embeddings.client.create(
#     input = "보장 생명보험",
#     engine=eng,
#     # engine="text-similarity-ada-001",
#     # engine="text-similarity-curie-001",
# )

# inp = res['data'][0]['embedding']

# db = []
# for ins in ["(무)생명보험(보장형)3", "(무)실손의료비보험(갱신형)2", "(무)실손의료비보험(보장형)3"]:
#     res = llm_helper.embeddings.client.create(
#         input = ins,
#         engine=eng,
#         # engine="text-similarity-ada-001",
#         # engine="text-similarity-curie-001",
#     )

#     db.append([ins, res['data'][0]['embedding']])

# for ins, vec in db:
#     similarity = cos_sim(inp, vec)
#     print(ins, ":", similarity)
# exit()

# 11111111111111111111111111111111111111111111
# 보험명 들어오면, 가장 유사한 보험명 뽑아내고?? 년도는?


import ast
import hashlib
from datetime import datetime
from urllib.parse import quote, unquote

insurance_name = '보장성 실손보험'
insurance_date = '199905'

similar_insurance = llm_helper.vector_store.similarity_search_with_score_insurance(insurance_name, "*", index_name="insurance-index", k=4)
best_insurance = similar_insurance.docs[0]


sell_date = []
date_list = [str(i) for i in ast.literal_eval(best_insurance.date)]
date_list.append("현재")

# 유사도로 검색한 보험을 해당 날짜에 팔지 않았따면?

for idx in range(1, len(date_list)):
    sell_date.append((date_list[idx-1], date_list[idx]))

date_key = None
for start, end in sell_date:
    if start <= insurance_date < end:
        print(start + " ~ " + end)
        date_key = start

if date_key is None:
    date_key = sell_date[-1][0]

print("입력된 보험 : ", insurance_name)

insurance_key = unquote(best_insurance.insurance)
print("가장 유사한 보험 : ", insurance_key)

print("date_key : ", date_key)



print("팔던 날짜 : ", sell_date)

candidate_insurance = [unquote(ins.insurance) for ins in similar_insurance.docs[1:]]

print("유사한 보험 : ", candidate_insurance)



print("찾기 시작.")
key = quote(insurance_key) + ":" + date_key
print("key : ", key)
hash_key = hashlib.sha1(key.encode('utf-8')).hexdigest()
print("hash key : ", hash_key)
res = llm_helper.get_semantic_answer_lang_chain("돈 얼마야", "", hash_key)

print(res)

exit()
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