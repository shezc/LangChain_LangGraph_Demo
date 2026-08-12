# 练习 04

1. 再声明 `multiply(a: int, b: int)` 工具。
2. 把 `add` 和 `multiply` 一起 `bind_tools`。
3. 问模型：「(6 + 7) * 3 等于多少？请用工具分步算。」
4. 遍历 `tool_calls`，在本地执行对应工具并打印每次结果。
5. 额外写一条 LCEL 链：把用户问题翻译成英文后再交给模型用一句话回答（可用两个 prompt，或一个 prompt 完成「先译后答」）。

对照 `solution.py`。不必在本课实现完整的 tool-calling 循环（那是第 05 / 08 课）。
