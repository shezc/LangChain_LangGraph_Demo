# 01 · Chat Model

## 目标

- 用 OpenRouter 创建 `ChatOpenAI`
- 区分 `invoke`（一次返回）和 `stream`（逐 token）

## 要点

LangChain 把各家模型收成统一的 Chat Model 接口。本仓库通过 OpenAI 兼容协议指向 `https://openrouter.ai/api/v1`，换模型只改 `.env` 里的 `OPENROUTER_MODEL`。

`invoke` 适合脚本和批处理；`stream` 适合交互式输出。

## 文档

- [Models](https://docs.langchain.com/oss/python/langchain/models)
- [OpenRouter](https://openrouter.ai/docs)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`，最后对照 `solution.py`。
