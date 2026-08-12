# 练习 09

1. 使用同一个 compiled graph 和 MemorySaver。
2. `thread_id=alpha`：先说「我最喜欢的颜色是蓝」，再问「我最喜欢什么颜色？」
3. `thread_id=beta`：直接问「我最喜欢什么颜色？」
4. 打印两次回答，确认 beta 并不知道蓝色（记忆按线程隔离）。

对照 `solution.py`。
