import streamlit as st
import os
from utilities.helper import LLMHelper
import numpy as np

llm_helper = LLMHelper()



# 11111111111111111111111111111111111111111111
# 보험명 들어오면, 가장 유사한 보험명 뽑아내고?? 년도는?


# insurance:8546e2663fa3cd3f0e0ddf2c30de19a0be538470:20210331
result = llm_helper.vector_store.similarity_search_with_score_insurance("보험", "*", index_name="insurance-index", k=1000)
print(result)


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