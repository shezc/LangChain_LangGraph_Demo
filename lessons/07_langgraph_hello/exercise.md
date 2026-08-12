# 练习 07

在 chatbot 之后增加第二个节点 `summarize`：

1. 读取对话里最后一条 AI 回复
2. 再调一次模型，把它压缩成不超过 10 个字
3. 边为 `START → chatbot → summarize → END`

跑一遍并打印全部 messages。对照 `solution.py`。
