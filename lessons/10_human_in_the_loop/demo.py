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
    return {"pending_action": "向 acct-001 退款 100 元"}


def review(state: State) -> dict:
    decision = interrupt(
        {
            "question": "是否批准该操作？回复 yes 或 no",
            "action": state["pending_action"],
        }
    )
    return {"decision": str(decision).strip().lower()}


def route(state: State) -> Literal["execute", "reject"]:
    if state.get("decision") in {"yes", "y", "approve"}:
        return "execute"
    return "reject"


def execute(state: State) -> dict:
    return {"messages": [AIMessage(content=f"已执行：{state['pending_action']}")]}


def reject(state: State) -> dict:
    return {"messages": [AIMessage(content="已拒绝，未执行任何操作。")]}


graph = StateGraph(State)
graph.add_node("propose", propose)
graph.add_node("review", review)
graph.add_node("execute", execute)
graph.add_node("reject", reject)
graph.add_edge(START, "propose")
graph.add_edge("propose", "review")
graph.add_conditional_edges("review", route)
graph.add_edge("execute", END)
graph.add_edge("reject", END)
app = graph.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "refund-1"}}

print_divider("第一次 invoke：会在 review 暂停")
paused = app.invoke({"messages": []}, config=config)
print("interrupt:", paused.get("__interrupt__"))

print_divider("人工批准后 resume")
done = app.invoke(Command(resume="yes"), config=config)
print(message_text(done["messages"][-1]))
