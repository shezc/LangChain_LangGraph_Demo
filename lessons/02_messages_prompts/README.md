# 02 · Messages 与 Prompt Template

## 目标

- 使用 `SystemMessage` / `HumanMessage` / `AIMessage` 表达多轮对话
- 用 `ChatPromptTemplate` 把变量填进提示词

## 要点

Chat Model 吃的是 **消息列表**，不是单纯的字符串。System 定角色，Human 是用户，AI 是模型历史回复。模板让同一套提示可以复用不同输入。

## 文档

- [Messages](https://docs.langchain.com/oss/python/langchain/messages)
- [Prompt templates](https://python.langchain.com/docs/concepts/prompt_templates/)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`。
