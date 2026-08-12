# 11 · 多 Agent

## 目标

- 拆成研究员 / 写手两个节点（不同角色、不同提示词）
- 用 supervisor 决定下一步：调研、撰写或结束
- 限制步数，避免路由死循环

## 要点

多 Agent 不是「多个模型」这么简单，关键是 **谁先说话、何时交接、共享什么 State**。Supervisor 模式由一个节点当调度；也有 handoff、swarm 等变体。本课用最小 supervisor，便于看清图结构。

## 文档

- [Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [LangGraph multi-agent](https://docs.langchain.com/oss/python/langgraph/multi-agent)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`。
