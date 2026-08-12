# 05 · LangChain Agent

## 目标

- 用 `create_agent` 搭一个会循环调用工具的 Agent
- 看清「模型选工具 → 执行 → 再思考」直到给出最终回答

## 要点

第 04 课只演示了「提出一次 tool call」。Agent 把这件事做成循环：只要回复里还有 `tool_calls`，就执行工具并把结果作为 `ToolMessage` 喂回去。LangChain 的 `create_agent` 底层就是 LangGraph；需要精细控制时，从第 07 课开始自己画图。

## 文档

- [Agents](https://docs.langchain.com/oss/python/langchain/agents)
- [create_agent](https://reference.langchain.com/python/langchain/agents/factory/create_agent)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`。
