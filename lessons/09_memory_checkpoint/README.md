# 09 · 记忆与 Checkpoint

## 目标

- 编译图时传入 `MemorySaver`
- 用 `thread_id` 区分会话
- 多次 `invoke` 仍能记住上文

## 要点

没有 checkpointer 时，每次 `invoke` 都是一次全新运行。加上 checkpointer 后，同一 `thread_id` 会把 State 续上；不同 thread 互不干扰。这是短期记忆、HITL 和故障恢复的基础。

## 文档

- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Memory](https://docs.langchain.com/oss/python/concepts/memory)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`。
