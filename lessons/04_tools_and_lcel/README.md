# 04 · Tools 与 LCEL

## 目标

- 用 `@tool` 声明可被模型调用的函数
- 用 `bind_tools` 把工具挂到模型上
- 用 LCEL 的 `|` 把 prompt、模型、解析器连成链

## 要点

工具是模型的「手」：模型决定调用哪个函数、传什么参数，真正执行仍是你的 Python 代码。LCEL（LangChain Expression Language）用管道组合可运行组件，适合线性流程；循环和分支交给后面的 Agent / LangGraph。

## 文档

- [Tools](https://docs.langchain.com/oss/python/langchain/tools)
- [LCEL](https://python.langchain.com/docs/concepts/lcel/)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`。
