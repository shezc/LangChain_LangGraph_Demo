# 07 · LangGraph Hello

## 目标

- 定义 `StateGraph` 与 `MessagesState`
- 添加节点和 `START` / `END` 边
- `compile` 后 `invoke`

## 要点

图 = 节点（函数）+ 边（流转）+ 共享 State。节点返回要**更新**的字段，而不是整份状态。`MessagesState` 自带 `messages` 列表，默认用追加 reducer。

先画最小图，再叠加工具、记忆和人工确认。

## 文档

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`。
