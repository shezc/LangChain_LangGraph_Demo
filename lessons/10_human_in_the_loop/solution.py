import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import Command, interrupt

from src.common.pretty import print_divider, message_text


class State(TypedDict):
    messages: Annotated[list, add_messages]
    pending_action: str
    decision: str


def propose(state: State) -> dict:
    return {"pending_action": "删除表 demo_users"}


def review(state: State) -> dict:
    decision = interrupt(
        {
            "question": "是否批准该操作？回复 yes 或 no",
            "action": state["pending_action"],
        }
    )
    return {"decision": str(decision).strip().lower()}


def route(state: State) -> Literal["execute", "reject"]:
    return "execute" if state.get("decision") in {"yes", "y", "approve"} else "reject"


def execute(state: State) -> dict:
    return {"messages": [AIMessage(content=f"已执行：{state['pending_action']}")]}


def reject(state: State) -> dict:
    return {"messages": [AIMessage(content="已拒绝，未执行任何操作。")]}


builder = StateGraph(State)
builder.add_node("propose", propose)
builder.add_node("review", review)
builder.add_node("execute", execute)
builder.add_node("reject", reject)
builder.add_edge(START, "propose")
builder.add_edge("propose", "review")
builder.add_conditional_edges("review", route)
builder.add_edge("execute", END)
builder.add_edge("reject", END)
app = builder.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "delete-1"}}
paused = app.invoke({"messages": []}, config=config)
print_divider("interrupt")
print(paused.get("__interrupt__"))

done = app.invoke(Command(resume="no"), config=config)
print_divider("最终")
print(message_text(done["messages"][-1]))
