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
from src.common.pretty import print_divider, message_text, print_messages

try:
    from langgraph.prebuilt import ToolNode, tools_condition
except ImportError:
    from langchain.tools import ToolNode
    from langchain.tools.tool_node import tools_condition


@tool
def get_weather(city: str) -> str:
    """查询模拟天气。"""
    demo = {"杭州": "小雨 18°C", "北京": "晴 26°C", "上海": "阴 22°C"}
    return demo.get(city, f"{city}：多云 20°C（模拟）")


@tool
def search(query: str) -> str:
    """模拟知识检索。"""
    return f"检索「{query}」：教学助手应先查工具，再总结，发信前必须人工确认。"


@tool
def send_message(to: str, body: str) -> str:
    """发送消息。执行前会暂停等待人工批准。"""
    decision = interrupt({"to": to, "body": body, "ask": "发送这条消息吗？yes/no"})
    if str(decision).strip().lower() not in {"yes", "y"}:
        return "已取消发送"
    return f"已发送给 {to}：{body}"


tools = [get_weather, search, send_message]
llm = get_chat_model(temperature=0).bind_tools(tools)
system = SystemMessage(
    content=(
        "你是教学助手。查天气用 get_weather，查资料用 search，"
        "用户要求发消息时必须调用 send_message，不要假装已经发了。"
        "用中文简短回答。"
    )
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

config = {"configurable": {"thread_id": "capstone-demo"}}

print_divider("1) 问天气")
r1 = app.invoke({"messages": [HumanMessage(content="杭州今天天气如何？")]}, config=config)
print(message_text(r1["messages"][-1]))

print_divider("2) 同一线程：考记忆")
r2 = app.invoke({"messages": [HumanMessage(content="我刚才问的是哪个城市？")]}, config=config)
print(message_text(r2["messages"][-1]))

print_divider("3) 请求发信 → 应 interrupt")
paused = app.invoke(
    {
        "messages": [
            HumanMessage(content="把刚才的天气摘要发给 ops@example.com，调用 send_message。")
        ]
    },
    config=config,
)
print("interrupt:", paused.get("__interrupt__"))

print_divider("4) 批准发送")
done = app.invoke(Command(resume="yes"), config=config)
print_messages(done["messages"][-4:])
