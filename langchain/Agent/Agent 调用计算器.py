'''
阶段三：Agent 代理与工具调用
核心概念： 过去是我们写死流程（Chain），而 Agent 是让 LLM 根据用户的意图，自己决定要调用哪个工具（搜索、计算器、写代码、查数据库）
'''
from dotenv import load_dotenv;
from langchain_classic.agents import AgentExecutor,create_openai_functions_agent
from langchain_core.tools import tool
from langchain_classic import hub
from langchain_deepseek import ChatDeepSeek

# 1. 自定义一个工具 （甚至可以是一个查询你公司数据库python 函数）

@tool
def getWordLenght(word:str) -> int:
    ''' 返回单词的长度 '''
    return len(word)

tools = [getWordLenght]

# 加载环境变量
load_dotenv()

model = ChatDeepSeek(model="deepseek-chat", temperature=0);

# 2. 获取预设的 Prompt 模板(ReAct 模式)
# 这是从 LangChain 官方拉取的成熟 Prompt ,告诉 AI 怎么思考.
prompt = hub.pull("hwchase17/openai-functions-agent")

# 3. 初始化 Agent
agent = create_openai_functions_agent(model, tools, prompt)

# 4. 初始化执行器 (Executor) - 相当于 Agent 的运行环境
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. 测试
agent_executor.invoke({"input": "单词 'LangChain' 的长度是多少？"})