# 06 · RAG 基础

## 目标

- 把本地文档切成 chunk
- 写入向量库并按问题检索
- 把检索结果塞进 prompt，让模型基于资料回答

## 要点

RAG = Retrieval Augmented Generation。模型本身没有你的私有文档，先检索再生成可减少胡编。本课用内存向量库 + 哈希向量，避免再调一套 Embedding API；上线应换成真实 embedding 模型。

## 文档

- [RAG tutorial](https://docs.langchain.com/oss/python/langchain/rag)
- [Text splitters](https://python.langchain.com/docs/concepts/text_splitters/)

## 本课文件

语料在 `corpus/`。先跑 `demo.py`，再做 `exercise.md`。
