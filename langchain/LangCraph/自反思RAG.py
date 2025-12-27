'''
既然你两个都需要，那我们现在就把所有知识点串联起来，完成从“学习者”到“开发者”的终极跃迁。

一、 终极实战：基于 LangGraph 的“自反思 RAG”
这是目前最顶尖的 RAG 架构（Self-RAG）。它不再是简单地检索并回答，而是：检索 -> 检查相关性 -> 如果不相关则重写查询 -> 重新检索 -> 回答。
'''

from typing import List, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage

# 1. 定义状态
class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]
    re_try_count: int


# 2. 定义节点函数
def retrieve(state: GraphState):
    print(" --- 执行检索 ----")

    # 模拟检索逻辑
    return {"documents": ["LangGraph 是用于构建循环图的框架"], "question": state["question"]}


def grade_documents(state: GraphState):
    print(" --- 检查文档相关性 ----")

    # 实际开发中这里会用一个小的 LLM 链来判断
    doc_content = state["documents"][0]

    if "LangGraph" in doc_content:
       return "relevant"
    return "irrelevant"

def generate(state: GraphState):
    print(" --- 生成回答 ----")
    return {"generation": "根据文档，LangGraph 适合构建复杂的 AI 逻辑。"}

# 3. 构建工作流图

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

# 设置入口
workflow.set_entry_point("retrieve")


# 4. 设置条件边: 检查检索结果是否相关
workflow.add_conditional_edges(
    "retrieve",
    grade_documents,
    {
        "relevant": "generate",
        "irrelevant": "retrieve", # 如果不相关，可以回到检索节点（或增加重写逻辑）
    }
)

workflow.add_edge("generate", END)

# 编译运行
app = workflow.compile()
print(app.invoke({"question": "什么是 LangGraph？", "re_try_count": 0})["generation"])

