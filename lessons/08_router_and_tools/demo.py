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


tools = [get_weather]
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
            SystemMessage(content="需要天气时必须调用工具。"),
            HumanMessage(content="杭州天气如何？"),
        ]
    }
)
print_messages(result["messages"])
