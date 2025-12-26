
# 核心目标: 学习如何在一个链中并行处理数据。这在后面做 RAG（检索增强生成）时非常关键.
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough,RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek

# 加载环境变量
load_dotenv()

# 1. 定义模型
model = ChatDeepSeek(model="deepseek-chat", temperature=0)

# 初始化模拟组件
parser = StrOutputParser()

print("正在初始化...",parser)

# 假设我们要同时完成两个任务: 翻译 + 总结
summary_prompt = ChatPromptTemplate.from_template("用一句话总结{text}")
translate_prompt = ChatPromptTemplate.from_template("翻译成英文{text}")

# 构建并运行处理链
'''
- RunnableParallel ：创建一个并行处理链，包含两个子链：
    - summary 子链：接收输入文本 → 应用总结提示 → 模型生成 → 解析输出
    - translate 子链：接收输入文本 → 应用翻译提示 → 模型生成 → 解析输出
    - 管道操作符 | ：表示数据从左到右流动，将前一个组件的输出作为后一个组件的输入

## 技术亮点
1. 并行处理 ：通过 RunnableParallel 实现了多个任务的并行执行，提高了处理效率
2. 模块化设计 ：每个组件（提示模板、模型、解析器）都是独立的，可以灵活组合
3. 清晰的数据流 ：使用管道操作符 | 直观地展示了数据的流动路径
4. 统一的接口 ：所有组件都遵循Runnable接口，可以无缝组合
5. 可扩展性 ：可以轻松添加更多并行任务，只需在 RunnableParallel 中添加新的键值对

## 应用场景
- RAG系统 ：并行检索多个数据源，提高信息获取效率
- 多语言处理 ：同时将文本翻译成多种语言
- 多角度分析 ：同时从不同角度（如情感分析、主题提取）分析文本
- 多模态处理 ：并行处理文本、图像、音频等不同类型的数据
这个示例展示了LangChain框架的核心优势：通过简单的组合，就能构建出强大的并行处理链，为复杂应用开发提供了高效的解决方案
'''
combined_chain = RunnableParallel(
    summary = summary_prompt | model | parser,
    translate = translate_prompt | model | parser
)

# 运行
result = combined_chain.invoke({"text":"LangChain 是一个旨在简化使用大语言模型创建应用程序的框架。它提供了链、代理等核心概念。"})
print(result)



'''
## 核心目标
该文件旨在演示如何使用LangChain框架在单个链中 并行处理数据 ，这是实现RAG（检索增强生成）等复杂应用的关键技术基础



'''

