# 练习 12

在 capstone 助手上再加一项能力：

1. 新工具 `get_time(city: str)`，返回模拟本地时间
2. 用户问「杭州现在几点、天气怎样」时应调用天气和时间两个工具
3. 保持原有记忆和 `send_message` 的 HITL
4. 脚本里至少跑：问时间+天气 → 同线程追问城市 → 发信并 `resume=no`（确认可以取消）

对照 `solution.py`。做完后试着用自己的话画一张图：START、agent、tools、interrupt 分别在哪。
