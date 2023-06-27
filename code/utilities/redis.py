import ast
import json
import logging
import uuid
import hashlib
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Tuple

from langchain.vectorstores.redis import Redis, RedisVectorStoreRetriever
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.base import VectorStore
from langchain.schema import BaseRetriever


import numpy as np
import pandas as pd
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import VectorField, TagField, TextField

logger = logging.getLogger()

class RedisExtended(Redis):
    def __init__(
        self,
        redis_url: str,
        index_name: str,
        embedding_function: Callable,
        **kwargs: Any,
    ):
        super().__init__(redis_url, index_name, embedding_function)
        
        # Check if index exists
        try:
            self.client.ft("prompt-index").info()
        except: 
            # Create Redis Index
            self.create_prompt_index()

        # Check if index exists
        try:
            self.client.ft("synonym-index").info()
        except: 
            # Create Synonym Index
            self.create_synonym_index()

        try:
            self.client.ft("insurance-index").info()
        except:
            # Create insurance Index
            self.create_insurance_index()

        try:
            self.client.ft(self.index_name).info()
        except:
            # Create Redis Index
            self.create_index()

    def check_existing_index(self, index_name: str = None):
        try:
            self.client.ft(index_name if index_name else self.index_name).info()
            return True
        except:
            return False

    def delete_keys(self, keys: List[str]) -> None:
        for key in keys:
            self.client.delete(key)
    
    def delete_keys_pattern(self, pattern: str) -> None:
        keys = self.client.keys(pattern)
        self.delete_keys(keys)

    def create_index(self, prefix = "doc", distance_metric:str="COSINE"):
        content = TextField(name="content")
        metadata = TextField(name="metadata")
        content_vector = VectorField("content_vector",
                    "HNSW", {
                        "TYPE": "FLOAT32",
                        "DIM": 1536,
                        "DISTANCE_METRIC": distance_metric,
                        "INITIAL_CAP": 1000,
                    })
        # Create index
        self.client.ft(self.index_name).create_index(
            fields = [content, metadata, content_vector],
            definition = IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
        )

    def get_index_results(self, prompt_index_name="prompt-index", number_of_results: int=3155):        

        base_query = f"f6707e308f4e88764ed7404a2a42964e80a8d01c"
        return_fields = ['insurance','date','content','metadata','content_vector']
        query = Query(base_query)\
            .paging(0, number_of_results)\
            .return_fields(*return_fields)\
            .dialect(2)

        # doc:embeddings:1f73d05ae20e00db294ec675b6f01f75be2fb855:20210331:217b2ffdcedbf80567253a8bddb2c5785457a722
        results = self.client.ft(self.index_name).search(query)
        # print(results)
        # results = self.client.ft("synonym-index").search("")
        # print(results)
        print(results.docs[0], len(results.docs))

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        embeddings: Optional[List[List[float]]] = None,
        keys: Optional[List[str]] = None,
        batch_size: int = 1000,
        **kwargs: Any,
    ) -> List[str]:
        """Add more texts to the vectorstore.

        Args:
            texts (Iterable[str]): Iterable of strings/text to add to the vectorstore.
            metadatas (Optional[List[dict]], optional): Optional list of metadatas.
                Defaults to None.
            embeddings (Optional[List[List[float]]], optional): Optional pre-generated
                embeddings. Defaults to None.
            keys (Optional[List[str]], optional): Optional key values to use as ids.
                Defaults to None.
            batch_size (int, optional): Batch size to use for writes. Defaults to 1000.

        Returns:
            List[str]: List of ids added to the vectorstore
        """
        import numpy as np

        def _redis_key(prefix: str) -> str:
            """Redis key schema for a given prefix."""
            return f"{prefix}:{uuid.uuid4().hex}"

        def _redis_prefix(index_name: str) -> str:
            """Redis key prefix for a given index."""
            return f"doc:{index_name}"

        content_key = "content"
        metadata_key = "metadata"
        vector_key = "content_vector"
        insurance_key = "insurance"
        date_key = "date"

        ids = []
        prefix = _redis_prefix(self.index_name)

        # Write data to redis
        pipeline = self.client.pipeline(transaction=False)
        for i, text in enumerate(texts):
            # Use provided values by default or fallback
            key = keys[i] if keys else _redis_key(prefix)
            metadata = metadatas[i] if metadatas else {}
            insurance = metadata.get("insurance", "")
            date = metadata.get("date", "")
            
            embedding = embeddings[i] if embeddings else self.embedding_function(text)
            pipeline.hset(
                key,
                mapping={
                    content_key: text,
                    insurance_key: insurance,
                    date_key: date,
                    vector_key: np.array(embedding, dtype=np.float32).tobytes(),
                    metadata_key: json.dumps(metadata),
                },
            )
            ids.append(key)

            # Write batch
            if i % batch_size == 0:
                pipeline.execute()

        # Cleanup final batch
        pipeline.execute()
        return ids


    # Prompt management
    def create_prompt_index(self, index_name="prompt-index", prefix = "prompt"):
        result = TextField(name="result")
        filename = TextField(name="filename")
        prompt = TextField(name="prompt")
        # Create index
        self.client.ft(index_name).create_index(
            fields = [result, filename, prompt],
            definition = IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
        )

    def add_prompt_result(self, id, result, filename="", prompt=""):
        self.client.hset(
            f"prompt:{id}",
            mapping={
                "result": result,
                "filename": filename,
                "prompt": prompt
            }
        )

    def get_prompt_results(self, prompt_index_name="prompt-index", number_of_results: int=3155):
        base_query = f'*'
        return_fields = ['id','result','filename','prompt']
        query = Query(base_query)\
            .paging(0, number_of_results)\
            .return_fields(*return_fields)\
            .dialect(2)
        results = self.client.ft(prompt_index_name).search(query)
        if results.docs:
            return pd.DataFrame(list(map(lambda x: {'id' : x.id, 'filename': x.filename, 'prompt': x.prompt, 'result': x.result.replace('\n',' ').replace('\r',' '),}, results.docs))).sort_values(by='id')
        else:
            return pd.DataFrame()

    def delete_prompt_results(self, prefix="prompt*"):
        self.delete_keys_pattern(pattern=prefix)


    # synonym management
    def create_synonym_index(self, index_name="synonym-index", prefix = "synonym"):
        writer = TextField(name="writer")
        regdate = TextField(name="regdate")
        title = TextField(name="title")
        synonymList = TextField(name="synonymList")
        # Create index
        self.client.ft(index_name).create_index(
            fields = [writer, regdate, title, synonymList],
            definition = IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
        )

    def add_synonym_result(self, id, writer="", regdate="", title="", synonymList=""):
        self.client.hset(
            f"synonym:{id}",
            mapping={
                "writer": writer,
                "regdate": regdate,
                "title": title,
                "synonymList":str(synonymList)
            }
        )

    def get_synonym_results(self, prompt_index_name="synonym-index", number_of_results: int=3155):
        base_query = f'*'
        return_fields = ['id','writer','regdate','title', 'synonymList']
        query = Query(base_query)\
            .paging(0, number_of_results)\
            .return_fields(*return_fields)\
            .dialect(2)

        results = self.client.ft(prompt_index_name).search(query)
        if results.docs:
            return pd.DataFrame(list(map(lambda x: {'id' : x.id, 'writer': x.writer, 'regdate': x.regdate, 'title': x.title, 'synonymList': ast.literal_eval(x.synonymList)}, results.docs))).sort_values(by='id')
        else:
            return pd.DataFrame()


    # insurance management
    def add_insurance_info(
        self,
        insurance: str,
        date: str,
    ):
        # Write data to redis
        embed_insurance = self.embedding_function(insurance)
        
        insurance_key = "insurance"
        date_key = "date"
        vector_key = "content_vector"

        insurance_hash_key = hashlib.sha1(insurance.encode('utf-8')).hexdigest()

        key = f"insurance:{insurance_hash_key}"

        # 기존 date 가져오기.
        if self.client.hget(key, date_key):
            date_list = ast.literal_eval(self.client.hget(key, date_key).decode())
            if int(date) not in date_list:
                date_list.append(int(date))
                date_list.sort()
            date = str(date_list)
        else:
            date = "[" + date + "]"

        pipeline = self.client.pipeline(transaction=False)

        pipeline.hset(
            key,
            mapping={
                insurance_key: insurance,
                date_key: date,
                vector_key: np.array(embed_insurance, dtype=np.float32).tobytes(),
            },
        )

        # Cleanup final batch
        pipeline.execute()


    def create_insurance_index(self, index_name="insurance-index", prefix = "insurance", distance_metric:str="COSINE"):
        insurance = TextField(name="insurance")
        date = TextField(name="date")
        content_vector = VectorField("content_vector",
                    "HNSW", {
                        "TYPE": "FLOAT32",
                        "DIM": 1536,
                        "DISTANCE_METRIC": distance_metric,
                        "INITIAL_CAP": 1000,
                    })

        # Create index
        self.client.ft(index_name).create_index(
            fields = [insurance, date, content_vector],
            definition = IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
        )

    def get_insurance_info(self, prompt_index_name="insurance-index", number_of_results: int=3155):
        base_query = f'*'
        return_fields = ['id','insurance','date','content_vector']
        query = Query(base_query)

        results = self.client.ft(prompt_index_name).search(query)
        
        if results.docs:
            return pd.DataFrame(list(map(lambda x: {'id' : x.id, 'insurance': x.insurance, 'date': x.date, 'content_vector': x.content_vector}, results.docs))).sort_values(by='id')
        else:
            return pd.DataFrame()

    
    
    def similarity_search_with_score_insurance(
        self, query: str, hash_key: str, index_name: str = "insurance-index", k: int = 4
    ) -> List[Tuple[str, float]]:
        """
        보험 명을 입력받았을 때, redis db 안에 있는 가장 유사한 보험명 리턴
        """
        
        try:
            from redis.commands.search.query import Query
        except ImportError:
            raise ValueError(
                "Could not import redis python package. "
                "Please install it with `pip install redis`."
            )

        # Creates embedding vector from user query
        embedding = self.embedding_function(query)

        # Prepare the Query
        return_fields = ["insurance", "date", "vector_score"]
        vector_field = "content_vector"
        hybrid_fields = hash_key
        base_query = (
            f"{hybrid_fields}=>[KNN {k} @{vector_field} $vector AS vector_score]"
        )
        redis_query = (
            Query(base_query)
            .return_fields(*return_fields)
            .sort_by("vector_score")
            .paging(0, k)
            .dialect(2)
        )
        params_dict: Mapping[str, str] = {
            "vector": np.array(embedding)  # type: ignore
            .astype(dtype=np.float32)
            .tobytes()
        }

        # perform vector search
        results = self.client.ft(index_name).search(redis_query, params_dict)
        return results


    def as_retriever(self, **kwargs: Any) -> BaseRetriever:
        return KyoboRedisVectorStoreRetriever(vectorstore=self, **kwargs)


    def similarity_search(
        self, query: str, hash_key:str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        """
        Returns the most similar indexed documents to the query text.

        Args:
            query (str): The query text for which to find similar documents.
            k (int): The number of documents to return. Default is 4.

        Returns:
            List[Document]: A list of documents that are most similar to the query text.
        """
        docs_and_scores = self.similarity_search_with_score(query, hash_key, k=k)
        return [doc for doc, _ in docs_and_scores]

    def similarity_search_with_score(
        self, query: str, hash_key:str, k: int = 4
    ) -> List[Tuple[Document, float]]:
        """Return docs most similar to query.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.

        Returns:
            List of Documents most similar to the query and score for each
        """
        try:
            from redis.commands.search.query import Query
        except ImportError:
            raise ValueError(
                "Could not import redis python package. "
                "Please install it with `pip install redis`."
            )

        # Creates embedding vector from user query
        embedding = self.embedding_function(query)
        k = 1000
        # Prepare the Query
        return_fields = ["metadata", "content", "vector_score"]
        vector_field = "content_vector"
        hybrid_fields = hash_key
        base_query = (
            f"{hybrid_fields}=>[KNN {k} @{vector_field} $vector AS vector_score]"
        )
        redis_query = (
            Query(base_query)
            .return_fields(*return_fields)
            .sort_by("vector_score")
            .paging(0, k)
            .dialect(2)
        )
        params_dict: Mapping[str, str] = {
            "vector": np.array(embedding)  # type: ignore
            .astype(dtype=np.float32)
            .tobytes()
        }

        # perform vector search
        results = self.client.ft(self.index_name).search(redis_query, params_dict)

        docs = [
            (
                Document(
                    page_content=result.content, metadata=json.loads(result.metadata)
                ),
                float(result.vector_score),
            )
            for result in results.docs
        ]
        print("테스트 전체 embedding 길이 : ", len(docs))
        return docs[:4]


class KyoboRedisVectorStoreRetriever(RedisVectorStoreRetriever):
    vectorstore: Redis
    search_type: str = "similarity"
    k: int = 4
    score_threshold: float = 0.4

    def get_relevant_documents(self, query: str, hash_key:str) -> List[Document]:
        if self.search_type == "similarity":
            docs = self.vectorstore.similarity_search(query, hash_key, k=self.k)
        elif self.search_type == "similarity_limit":
            docs = self.vectorstore.similarity_search_limit_score(
                query, k=self.k, score_threshold=self.score_threshold
            )
        else:
            raise ValueError(f"search_type of {self.search_type} not allowed.")
        return docs

