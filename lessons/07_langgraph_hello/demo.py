import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, MessagesState, StateGraph

from src.common.llm import get_chat_model
from src.common.pretty import print_divider, print_messages

llm = get_chat_model(temperature=0)


def chatbot(state: MessagesState) -> dict:
    reply = llm.invoke(state["messages"])
    return {"messages": [reply]}


graph = StateGraph(MessagesState)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
app = graph.compile()

print_divider("最小图")
result = app.invoke({"messages": [HumanMessage(content="用五个字介绍 LangGraph。")]})
print_messages(result["messages"])
