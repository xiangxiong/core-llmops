# 基于 LangGraph 的自反思 RAG 解析

## 一、代码解析

### 1. 代码概述

这段代码实现了一个基于 LangGraph 的自反思 RAG（Retrieval-Augmented Generation）系统。自反思 RAG 是目前最顶尖的 RAG 架构之一，它不再是简单地检索并回答，而是形成了一个闭环：检索 -> 检查相关性 -> 如果不相关则重写查询 -> 重新检索 -> 回答。

### 2. 代码结构详解

#### 2.1 状态定义

```python
from typing import List, TypedDict

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]
    re_try_count: int
```

- **GraphState**：使用 TypedDict 定义了图的状态结构，包含四个关键字段：
  - `question`：用户的原始问题
  - `generation`：AI 生成的回答
  - `documents`：从检索系统获取的文档列表
  - `re_try_count`：重试次数，用于控制循环次数

#### 2.2 节点函数

```python
def retrieve(state: GraphState):
    print(" --- 执行检索 ----")
    # 模拟检索逻辑
    return {"documents": ["LangGraph 是用于构建循环图的框架"], "question": state["question"]}
```

- **retrieve 函数**：负责执行检索操作
  - 接收当前状态作为输入
  - 模拟实现了检索逻辑，返回相关文档
  - 更新状态中的 documents 字段

```python
def grade_documents(state: GraphState):
    print(" --- 检查文档相关性 ----")
    # 实际开发中这里会用一个小的 LLM 链来判断
    doc_content = state["documents"][0]
    if "LangGraph" in doc_content:
       return "relevant"
    return "irrelevant"
```

- **grade_documents 函数**：负责评估检索到的文档与问题的相关性
  - 接收当前状态作为输入
  - 简单模拟了相关性判断逻辑（实际应用中会使用 LLM）
  - 返回判断结果："relevant" 或 "irrelevant"

```python
def generate(state: GraphState):
    print(" --- 生成回答 ----")
    return {"generation": "根据文档，LangGraph 适合构建复杂的 AI 逻辑。"}
```

- **generate 函数**：负责生成最终回答
  - 接收当前状态作为输入
  - 基于检索到的相关文档生成回答
  - 更新状态中的 generation 字段

#### 2.3 工作流构建

```python
from langgraph.graph import StateGraph, END

# 构建工作流图
workflow = StateGraph(GraphState)

# 添加节点
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

# 设置入口
workflow.set_entry_point("retrieve")

# 设置条件边: 检查检索结果是否相关
workflow.add_conditional_edges(
    "retrieve",
    grade_documents,
    {
        "relevant": "generate",
        "irrelevant": "retrieve", # 如果不相关，可以回到检索节点（或增加重写逻辑）
    }
)

# 添加结束边
workflow.add_edge("generate", END)

# 编译运行
app = workflow.compile()
print(app.invoke({"question": "什么是 LangGraph？", "re_try_count": 0})["generation"])
```

- **工作流构建**：
  1. 创建 `StateGraph` 实例，指定状态类型为 `GraphState`
  2. 添加节点：retrieve 和 generate
  3. 设置入口点为 retrieve
  4. 添加条件边：从 retrieve 节点出发，根据 grade_documents 的结果决定下一步
     - 如果相关，进入 generate 节点
     - 如果不相关，返回 retrieve 节点重新检索
  5. 添加结束边：从 generate 节点到 END
  6. 编译工作流并执行

### 3. 执行流程

1. 用户输入问题："什么是 LangGraph？"
2. 进入 retrieve 节点，执行检索操作
3. 进入 grade_documents 函数，检查文档相关性
4. 如果文档相关，进入 generate 节点生成回答
5. 回答生成完成，流程结束
6. 如果文档不相关，返回 retrieve 节点重新检索

## 二、举一反三：扩展自反思 RAG 实现

下面是一个扩展的自反思 RAG 实现，增加了查询重写功能，更完整地展示了自反思 RAG 的核心逻辑：

```python
from typing import List, TypedDict
from langgraph.graph import StateGraph, END

# 1. 定义状态
class GraphState(TypedDict):
    question: str
    original_question: str
    rewritten_question: str
    generation: str
    documents: List[str]
    re_try_count: int
    max_retries: int

# 2. 定义节点函数
def retrieve(state: GraphState):
    print(f" --- 执行检索 (第 {state['re_try_count'] + 1} 次) ----")
    print(f"检索问题: {state['question']}")
    
    # 模拟检索逻辑
    if "LangGraph" in state["question"]:
        return {
            "documents": ["LangGraph 是用于构建循环图的框架，支持复杂的 AI 工作流设计。"], 
            "question": state["question"]
        }
    else:
        return {
            "documents": ["LangChain 是一个用于构建 LLM 应用的框架。"], 
            "question": state["question"]
        }

def grade_documents(state: GraphState):
    print(" --- 检查文档相关性 ----")
    doc_content = state["documents"][0]
    print(f"检索到的文档: {doc_content}")
    
    # 实际开发中这里会用一个小的 LLM 链来判断
    if "LangGraph" in doc_content and "LangGraph" in state["question"]:
       return "relevant"
    return "irrelevant"

def rewrite_query(state: GraphState):
    print(" --- 重写查询 ----")
    # 模拟查询重写逻辑
    return {
        "question": f"什么是 LangGraph？",
        "rewritten_question": f"什么是 LangGraph？",
        "re_try_count": state["re_try_count"] + 1
    }

def generate(state: GraphState):
    print(" --- 生成回答 ----")
    return {"generation": f"根据文档，{state['documents'][0]}"}

def should_retry(state: GraphState):
    print(f" --- 检查是否需要重试 (当前重试次数: {state['re_try_count']}) ----")
    return "retry" if state["re_try_count"] < state["max_retries"] else "stop"

# 3. 构建工作流图
workflow = StateGraph(GraphState)

# 添加节点
workflow.add_node("retrieve", retrieve)
workflow.add_node("rewrite_query", rewrite_query)
workflow.add_node("generate", generate)

# 设置入口
workflow.set_entry_point("retrieve")

# 设置条件边: 检查检索结果是否相关
workflow.add_conditional_edges(
    "retrieve",
    grade_documents,
    {
        "relevant": "generate",
        "irrelevant": "should_retry",  # 如果不相关，先检查是否需要重试
    }
)

# 设置重试条件边
workflow.add_conditional_edges(
    "should_retry",
    should_retry,
    {
        "retry": "rewrite_query",  # 需要重试，重写查询
        "stop": "generate"  # 达到最大重试次数，直接生成回答
    }
)

# 重写查询后回到检索节点
workflow.add_edge("rewrite_query", "retrieve")

# 添加结束边
workflow.add_edge("generate", END)

# 编译运行
app = workflow.compile()
result = app.invoke({
    "question": "什么是 LangGraph 框架？", 
    "original_question": "什么是 LangGraph 框架？",
    "re_try_count": 0,
    "max_retries": 2
})

print(f"\n最终回答: {result['generation']}")
```

### 扩展实现的改进点

1. **增加了查询重写功能**：当检索到的文档不相关时，会重写查询后重新检索
2. **增加了重试机制**：通过 `max_retries` 控制最大重试次数，避免无限循环
3. **保留了原始问题**：便于追踪查询演变过程
4. **更详细的日志输出**：便于调试和理解执行流程

## 三、业务应用场景

### 1. 客户服务系统

- **应用**：构建智能客服机器人，自动处理客户查询
- **价值**：
  - 当客户问题表述不清时，系统可以自动重写查询，提高回答准确率
  - 减少人工客服干预，降低运营成本
  - 提供一致的服务质量，不受人工客服情绪和能力影响

### 2. 企业知识管理

- **应用**：构建企业内部知识库问答系统
- **价值**：
  - 员工可以用自然语言查询企业政策、流程和技术文档
  - 系统可以自动评估文档相关性，确保回答的准确性
  - 支持复杂问题的多轮推理和检索

### 3. 教育辅导系统

- **应用**：构建智能教育辅导平台
- **价值**：
  - 学生可以用自己的语言提问，系统自动优化查询
  - 提供个性化的学习内容推荐
  - 支持复杂问题的逐步解答和推理

### 4. 医疗咨询系统

- **应用**：构建医疗健康咨询系统
- **价值**：
  - 患者可以用自然语言描述症状，系统自动优化查询
  - 检索相关医疗知识，提供初步建议
  - 提高医疗信息的可及性，缓解医疗资源紧张

### 5. 法律文书助手

- **应用**：构建法律文书生成和查询系统
- **价值**：
  - 律师可以用自然语言查询法律条文和案例
  - 系统自动优化查询，提高检索准确性
  - 辅助生成法律文书，提高工作效率

## 四、观点改进

### 1. 从"单向流程"到"闭环系统"

- **传统观点**：AI 系统是单向的，输入 -> 处理 -> 输出
- **新观点**：AI 系统应该是闭环的，输入 -> 处理 -> 评估 -> 优化 -> 重新处理 -> 输出
- **影响**：提高了系统的鲁棒性和准确性，能够处理模糊和复杂的输入

### 2. 从"静态检索"到"动态优化"

- **传统观点**：检索是一次性的，使用固定的查询词
- **新观点**：检索是动态的，可以根据检索结果不断优化查询
- **影响**：提高了检索的召回率和准确率，能够处理信息需求不明确的情况

### 3. 从"单一模型"到"多模块协作"

- **传统观点**：AI 系统依赖单一模型完成所有任务
- **新观点**：AI 系统由多个专业模块协作完成任务
- **影响**：提高了系统的灵活性和可维护性，便于针对不同任务优化不同模块

### 4. 从"无记忆系统"到"有状态系统"

- **传统观点**：AI 系统处理每个请求都是独立的，没有状态
- **新观点**：AI 系统应该维护状态，记录处理过程中的关键信息
- **影响**：支持复杂的多轮推理和上下文理解，提高了系统的智能水平

### 5. 从"开发者主导"到"系统自优化"

- **传统观点**：系统优化依赖开发者手动调整
- **新观点**：系统可以自动评估和优化自身性能
- **影响**：降低了系统维护成本，提高了系统的适应性和进化能力

## 五、总结

基于 LangGraph 的自反思 RAG 系统代表了当前 AI 应用开发的先进方向，它通过闭环设计、动态优化和多模块协作，显著提高了 AI 系统的准确性和鲁棒性。这一技术不仅可以应用于客户服务、知识管理等多个业务场景，还改变了我们对 AI 系统设计的认知。

学习和掌握自反思 RAG 技术，有助于我们构建更智能、更可靠的 AI 应用，同时也能改进我们对 AI 系统设计的观点，从单向流程转变为闭环系统，从静态检索转变为动态优化，从单一模型转变为多模块协作。

在未来的 AI 应用开发中，自反思 RAG 架构将扮演越来越重要的角色，帮助我们构建更接近人类思维方式的智能系统。