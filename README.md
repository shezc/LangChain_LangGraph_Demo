# LangChain + LangGraph 动手学习

按模块递进的 Python 课程：先掌握 LangChain 组件，再写高层 Agent，最后用 LangGraph 编排有状态的工作流。模型统一走 [OpenRouter](https://openrouter.ai/)（OpenAI 兼容接口）。

## 环境

需要 Python 3.11+，以及 **Pydantic v2**（请用本仓库虚拟环境，不要混用系统里的 Pydantic 1.x）。

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

复制密钥文件并填入你的 Key（没有 Key 时，需要调模型的脚本会提示后退出；[第 10 课 HITL](lessons/10_human_in_the_loop) 不调模型，可先跑通）：

```bash
copy .env.example .env
```

在 `.env` 中设置：

- `OPENROUTER_API_KEY`：https://openrouter.ai/keys
- `OPENROUTER_MODEL`：例如 `openai/gpt-4o-mini`，模型列表见 https://openrouter.ai/models

## 怎么学

每个模块在 `lessons/NN_xxx/`，固定四件套：

| 文件 | 用途 |
| --- | --- |
| `README.md` | 概念要点与本课目标 |
| `demo.py` | 先跑通的完整示例 |
| `exercise.md` | 练习题（先自己写） |
| `solution.py` | 参考实现（对照用） |

建议顺序：

1. 读本课 `README.md`
2. `python lessons/01_chat_model/demo.py`（把 `01_chat_model` 换成当前模块；未激活 venv 时用 `.\.venv\Scripts\python`）
3. 按 `exercise.md` 自己写代码（可新建 `my_solution.py`）
4. 对照 `solution.py`

卡住时直接说模块号（例如「讲一下 08」），可以继续讲解或加示例。

## 大纲

| 模块 | 主题 | 建议时长 |
| --- | --- | --- |
| [01_chat_model](lessons/01_chat_model) | ChatModel、invoke / stream | 0.5 天 |
| [02_messages_prompts](lessons/02_messages_prompts) | Message、ChatPromptTemplate | 0.5 天 |
| [03_structured_output](lessons/03_structured_output) | Pydantic 结构化输出 | 0.5 天 |
| [04_tools_and_lcel](lessons/04_tools_and_lcel) | `@tool`、LCEL 链 | 0.5 天 |
| [05_langchain_agent](lessons/05_langchain_agent) | 高层 Agent（tool-calling loop） | 1 天 |
| [06_rag_basics](lessons/06_rag_basics) | 切分、检索、RAG | 1 天 |
| [07_langgraph_hello](lessons/07_langgraph_hello) | StateGraph 最小图 | 1 天 |
| [08_router_and_tools](lessons/08_router_and_tools) | 条件边、手写 ReAct 图 | 1 天 |
| [09_memory_checkpoint](lessons/09_memory_checkpoint) | checkpointer、thread 记忆 | 1 天 |
| [10_human_in_the_loop](lessons/10_human_in_the_loop) | interrupt / 人工确认 | 1 天 |
| [11_multi_agent](lessons/11_multi_agent) | supervisor 多 Agent | 1–2 天 |
| [12_capstone](lessons/12_capstone) | 记忆 + 工具 + HITL 小助手 | 1–2 天 |

```text
LangChain 组件 ──► Agent / RAG ──► LangGraph 编排 ──► Capstone
   01-04              05-06            07-11              12
```

## 公共代码

- [`src/common/llm.py`](src/common/llm.py)：OpenRouter ChatModel
- [`src/common/env.py`](src/common/env.py)：加载 `.env`，缺 Key 时给出提示

## 可选：LangSmith

本课程不强制追踪。若要看调用链，在 `.env` 中打开 `LANGSMITH_TRACING` 并填入 LangSmith Key，参见 [LangSmith tracing](https://docs.langchain.com/langsmith/trace-with-langchain)。
