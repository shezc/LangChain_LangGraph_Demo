# 03 · 结构化输出

## 目标

- 用 Pydantic 定义输出 schema
- 用 `with_structured_output` 拿到对象而不是自由文本

## 要点

自由文本难解析。给模型一个 schema，它会按字段返回，适合抽取、分类、填表。字段的 `description` 就是给模型的说明。

## 文档

- [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`。
