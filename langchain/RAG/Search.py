from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek

# 加载环境变量
load_dotenv()

# 1.加载刚才建好的知识库并设为检索器
vectorstore = FAISS.load_local("./vectorstore", FakeEmbeddings(size=1536), allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# 1. 定义模型
model = ChatDeepSeek(model="deepseek-chat", temperature=0)

# 2. 定义 RAG 专用 Prompt
template = """
  {context}

  问题: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

# 3. 构建 RAG 链 
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 4. 提问
print(rag_chain.invoke("LangChain 最火的场景是什么？"))

