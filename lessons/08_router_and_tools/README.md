# 08 · 条件边与工具图

## 目标

- 用 `ToolNode` 执行工具
- 用 `tools_condition` 在「继续调工具」和「结束」之间路由
- 亲手搭出与 `create_agent` 等价的 ReAct 环

## 要点

条件边根据 State 决定下一跳。典型 Agent 图：

`agent ─(有 tool_calls)→ tools → agent`  
`agent ─(没有)→ END`

这就是第 05 课高层 Agent 揭开盖子后的样子。

## 文档

- [ToolNode](https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolNode)
- [Choosing APIs](https://docs.langchain.com/oss/python/langgraph/choosing-apis)

## 本课文件

先跑 `demo.py`，再做 `exercise.md`。
