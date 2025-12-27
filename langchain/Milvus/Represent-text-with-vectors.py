import hashlib
import numpy as np
import os
from dotenv import load_dotenv
from pymilvus import MilvusClient, DataType

load_dotenv()
# A valid token could be either
# - An API key, or 
# - A colon-joined cluster username and password, as in `user:pass`

# 1. Set up a Milvus client
client = MilvusClient(
    uri=os.getenv("CLUSTER_ENDPOINT"),
    token=os.getenv("TOKEN") 
)

# 自定义嵌入函数，生成1536维向量以匹配集合定义
class CustomEmbeddingFunction:
    def __init__(self, dim=1536):  # 调整维度为1536，匹配集合定义
        self.dim = dim
    
    def encode_documents(self, docs):
        vectors = []
        for doc in docs:
            # 使用哈希值生成固定长度的向量
            hash_value = hashlib.sha256(doc.encode('utf-8')).hexdigest()
            # 将哈希值转换为浮点数向量
            vector = []
            for i in range(0, len(hash_value), 8):
                segment = hash_value[i:i+8]
                vector.append(float(int(segment, 16)) / (16**8 - 1))
            # 调整向量维度到指定大小
            if len(vector) > self.dim:
                vector = vector[:self.dim]
            else:
                # 填充到指定维度
                vector += [0.0] * (self.dim - len(vector))
            vectors.append(np.array(vector))
        return vectors
    
    def encode_queries(self, queries):
        # 对于简单的嵌入函数，查询和文档可以使用相同的编码方法
        # 复杂模型可能会对查询和文档使用不同的编码逻辑
        return self.encode_documents(queries)

# 使用自定义嵌入函数，生成1536维向量
embedding_fn = CustomEmbeddingFunction(dim=1536)

# Text strings to search from.
docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
]

vectors = embedding_fn.encode_documents(docs);

# The output vector has 1536 dimensions, matching the collection
print("Dim:", embedding_fn.dim, vectors[0].shape)  # Dim: 1536 (1536,)

# 调整数据结构：
# 1. 移除手动指定的id（因为auto_id=True）
# 2. 只保留集合中定义的字段：vector、text、subject
# 3. 确保向量维度为1536
data = [
    { "vector": vectors[i], "text": docs[i], "subject": "history" }
    for i in range(len(vectors))
]

print("Data has", len(data), "entities, each with fields: ", data[0].keys())
print("Vector dim:", len(data[0]["vector"]))

# 插入数据到集合
res = client.insert(collection_name="example_collection", data=data)
print(res);

# 生成查询向量
query_vectors = embedding_fn.encode_queries(["Who is Alan Turing?"])
# If you don't have the embedding function you can use a fake vector to finish the demo:
# query_vectors = [ [ random.uniform(-1, 1) for _ in range(1536) ] ]

# 搜索数据，使用正确的集合名称 example_collection
res1 = client.search(
    collection_name="example_collection",  # 使用正确的集合名称
    data=query_vectors,  # query vectors
    limit=2,  # number of returned entities
    output_fields=["text", "subject"],  # specifies fields to be returned
)

print('res1', res1)