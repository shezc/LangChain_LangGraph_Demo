import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import START, MessagesState, StateGraph

from src.common.llm import get_chat_model
from src.common.pretty import print_messages

try:
    from langgraph.prebuilt import ToolNode, tools_condition
except ImportError:
    from langchain.tools import ToolNode
    from langchain.tools.tool_node import tools_condition


@tool
def get_weather(city: str) -> str:
    """查询模拟天气。"""
    demo = {"杭州": "小雨 18°C", "北京": "晴 26°C"}
    return demo.get(city, f"{city}：多云 20°C")


@tool
def search(query: str) -> str:
    """模拟网页搜索。"""
    return (
        "检索结果：LangGraph checkpointer 把每次图执行的 State 按 thread_id 存下来，"
        "用于多轮记忆、失败恢复和 human-in-the-loop。"
    )


tools = [get_weather, search]
llm = get_chat_model(temperature=0).bind_tools(tools)


def agent(state: MessagesState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


graph = StateGraph(MessagesState)
graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")
app = graph.compile()

result = app.invoke(
    {
        "messages": [
            SystemMessage(content="需要事实时调用工具，不要编造。"),
            HumanMessage(content="LangGraph 的 checkpointer 是做什么的？另外北京天气呢？"),
        ]
    }
)
print_messages(result["messages"])
