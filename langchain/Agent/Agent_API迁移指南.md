# LangChain Agent API 迁移指南

## 问题描述
在运行Agent相关代码时，遇到以下导入错误：

```
Traceback (most recent call last):
  File "/Users/apple/Desktop/python/llm-ops/core-llmops/langchain/Agent/Agent 调用计算器.py", line 6, in <module>
    from langchain.agents import AgentExecutor,create_openai_functions_agent
ImportError: cannot import name 'AgentExecutor' from 'langchain.agents' (/Users/apple/anaconda3/lib/python3.11/site-packages/langchain/agents/__init__.py)
```

## 根本原因
LangChain 1.1.x 版本进行了**重大架构重构**：
- 经典 Agent 功能从 `langchain.agents` 迁移到 `langchain_classic.agents`
- `hub` 模块从 `langchain` 迁移到 `langchain_classic`
- 模块化设计，分离经典功能与新功能

## 修复方案

### 1. 修复 Agent 相关导入

**原代码（错误）**：
```python
from langchain.agents import AgentExecutor,create_openai_functions_agent
```

**修复后（正确）**：
```python
from langchain_classic.agents import AgentExecutor,create_openai_functions_agent
```

### 2. 修复 hub 模块导入

**原代码（错误）**：
```python
from langchain import hub
```

**修复后（正确）**：
```python
from langchain_classic import hub
```

## 修复结果

修复后，脚本可以成功运行：

```
> Entering new AgentExecutor chain...
单词 "LangChain" 的长度是 **9 个字符**（包括大写字母 L 和 C）。
> Finished chain.
```

## 迁移策略总结

| 旧 API | 新 API | 适用版本 |
|-------|--------|----------|
| `langchain.agents` | `langchain_classic.agents` | LangChain 1.1.x+ |
| `langchain.hub` | `langchain_classic.hub` | LangChain 1.1.x+ |

## 最佳实践

1. **新项目**：建议使用 LangChain 1.0+ 的新 API
2. **旧项目**：通过替换导入路径实现平滑迁移
3. **版本管理**：在 `requirements.txt` 中指定兼容的 LangChain 版本
4. **文档参考**：查阅 [LangChain 官方迁移文档](https://python.langchain.com/docs/guides/migration/) 获取最新信息

## 常见问题

### Q: 为什么会出现这个错误？
A: 因为 LangChain 1.1.x 版本对 Agent 功能进行了模块化重构，将经典功能迁移到了 `langchain_classic` 命名空间。

### Q: 除了 Agent 功能，还有哪些模块受到影响？
A: 还有 `hub`、`chains` 等经典模块也进行了类似的迁移。

### Q: 如何查看当前安装的 LangChain 版本？
A: 使用命令 `pip show langchain` 可以查看当前版本。

### Q: 迁移后是否会影响其他功能？
A: 迁移后，原有功能保持不变，只是导入路径发生了变化。

## 代码示例

**完整修复后的代码**：

```python
from dotenv import load_dotenv;
from langchain_classic.agents import AgentExecutor,create_openai_functions_agent
from langchain_core.tools import tool
from langchain_classic import hub
from langchain_deepseek import ChatDeepSeek

@tool
def getWordLenght(word:str) -> int:
    ''' 返回单词的长度 '''
    return len(word)

tools = [getWordLenght]

load_dotenv()

model = ChatDeepSeek(model="deepseek-chat", temperature=0);

prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_functions_agent(model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "单词 'LangChain' 的长度是多少？"})
```

## 结论

通过将导入路径从 `langchain` 替换为 `langchain_classic`，可以成功解决 LangChain 1.1.x 版本中的 Agent 导入错误。这种迁移方式保证了旧代码的兼容性，同时支持新项目使用 LangChain 的最新功能。