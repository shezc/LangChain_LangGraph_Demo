# 练习 10

复制 demo 的图结构，改成「删除数据库」场景：

1. `pending_action` 设为 `删除表 demo_users`
2. 第一次 `invoke` 后打印 interrupt payload
3. 用 `Command(resume="no")` 恢复
4. 确认最终消息是拒绝、没有执行

对照 `solution.py`。
