import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph

from src.common.llm import get_chat_model
from src.common.pretty import print_divider, message_text

llm = get_chat_model(temperature=0)


def chatbot(state: MessagesState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


graph = StateGraph(MessagesState)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
app = graph.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "user-a"}}

print_divider("第一轮：告诉名字")
r1 = app.invoke(
    {"messages": [HumanMessage(content="我叫阿白，请记住。以后用这个名字称呼我。")]},
    config=config,
)
print(message_text(r1["messages"][-1]))

print_divider("第二轮：同一 thread，应能叫出名字")
r2 = app.invoke(
    {"messages": [HumanMessage(content="我叫什么？")]},
    config=config,
)
print(message_text(r2["messages"][-1]))
