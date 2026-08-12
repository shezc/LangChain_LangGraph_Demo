# 10 · Human-in-the-loop

## 目标

- 在节点里调用 `interrupt()` 暂停图
- 用 `Command(resume=...)` 带着人的决定继续
- 理解 HITL **必须**配合 checkpointer

## 要点

敏感操作（转账、发邮件、删数据）不应由模型直接落锤。`interrupt` 把 payload 抛给调用方；进程可以退出，因为 checkpoint 已保存。恢复时从 `interrupt()` 那一行继续，返回值就是 `resume` 的内容。

## 文档

- [Human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [Command](https://docs.langchain.com/oss/python/langgraph/graph-api)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`。
