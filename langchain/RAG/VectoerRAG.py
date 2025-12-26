from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import FakeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 构建你的第一个，本地知识库.
# 核心目标： 理解文本是如何变成向量并存进数据库的.

# 1.原始长文本 (模拟你的文档)
raw_text = """
LangChain 实战指南：
1. LCEL 是核心语法。
2. RAG 是目前最火的落地场景。
3. Agent 代理是未来的高级形态。
"""

# 2. 切分文档(把大书拆成小页)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.create_documents([raw_text])

# 3. 向量化并存储到本地 (把文字变成 AI 能懂的数字坐标)
# 使用FakeEmbeddings进行测试，无需网络连接
embeddings = FakeEmbeddings(size=1536)
vectorstore = FAISS.from_documents(docs, embeddings)

# 4. 存为本地索引文件，下载直接加载
vectorstore.save_local("vectorstore")
print("知识库已成功建立！")