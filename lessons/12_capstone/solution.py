import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.types import Command, interrupt

from src.common.llm import get_chat_model
from src.common.pretty import print_divider, message_text

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
def get_time(city: str) -> str:
    """查询模拟本地时间。"""
    demo = {"杭州": "09:15", "北京": "09:15", "纽约": "21:15"}
    return demo.get(city, f"{city}：12:00（模拟）")


@tool
def send_message(to: str, body: str) -> str:
    """发送消息，执行前需人工批准。"""
    decision = interrupt({"to": to, "body": body, "ask": "发送？yes/no"})
    if str(decision).strip().lower() not in {"yes", "y"}:
        return "已取消发送"
    return f"已发送给 {to}：{body}"


tools = [get_weather, get_time, send_message]
llm = get_chat_model(temperature=0).bind_tools(tools)
system = SystemMessage(
    content="天气用 get_weather，时间用 get_time，发信用 send_message。用中文简短回答。"
)


def agent(state: MessagesState) -> dict:
    return {"messages": [llm.invoke([system, *state["messages"]])]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
app = builder.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "capstone-ex"}}

print_divider("时间 + 天气")
r1 = app.invoke(
    {"messages": [HumanMessage(content="杭州现在几点、天气怎样？")]},
    config=config,
)
print(message_text(r1["messages"][-1]))

print_divider("记忆")
r2 = app.invoke({"messages": [HumanMessage(content="我问的是哪座城市？")]}, config=config)
print(message_text(r2["messages"][-1]))

print_divider("发信并拒绝")
paused = app.invoke(
    {"messages": [HumanMessage(content="把摘要发给 ops@example.com，调用 send_message。")]},
    config=config,
)
print("interrupt:", paused.get("__interrupt__"))
done = app.invoke(Command(resume="no"), config=config)
print(message_text(done["messages"][-1]))
