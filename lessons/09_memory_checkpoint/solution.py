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

alpha = {"configurable": {"thread_id": "alpha"}}
beta = {"configurable": {"thread_id": "beta"}}

app.invoke(
    {"messages": [HumanMessage(content="我最喜欢的颜色是蓝。")]},
    config=alpha,
)
r_alpha = app.invoke(
    {"messages": [HumanMessage(content="我最喜欢什么颜色？")]},
    config=alpha,
)
r_beta = app.invoke(
    {"messages": [HumanMessage(content="我最喜欢什么颜色？")]},
    config=beta,
)

print_divider("alpha（有记忆）")
print(message_text(r_alpha["messages"][-1]))
print_divider("beta（无上文）")
print(message_text(r_beta["messages"][-1]))
