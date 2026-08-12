import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from src.common.llm import get_chat_model
from src.common.pretty import print_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    next: str
    steps: int


class Route(BaseModel):
    next: Literal["researcher", "writer", "FINISH"] = Field(
        description="下一步：researcher 调研，writer 撰稿，FINISH 结束"
    )


@tool
def search(query: str) -> str:
    """模拟搜索。"""
    return (
        f"关于「{query}」的笔记：LangGraph 用节点和边编排 Agent；"
        "checkpointer 按 thread 保存 State；HITL 用 interrupt 暂停敏感步骤。"
    )


llm = get_chat_model(temperature=0)
router_llm = llm.with_structured_output(Route)


def supervisor(state: State) -> dict:
    steps = int(state.get("steps") or 0) + 1
    if steps >= 5:
        return {"next": "FINISH", "steps": steps}
    route = router_llm.invoke(
        [
            SystemMessage(
                content=(
                    "你是调度。还没有研究员笔记就去 researcher；"
                    "有笔记但没有成稿就去 writer；成稿已在对话里就 FINISH。"
                    "不要自己写正文。"
                )
            ),
            *state["messages"],
        ]
    )
    return {"next": route.next, "steps": steps}


def researcher(state: State) -> dict:
    question = state["messages"][0].content
    notes = search.invoke(str(question))
    reply = llm.invoke(
        [
            SystemMessage(content="你是研究员。根据检索笔记列出3条中文要点，不要写成文章。"),
            HumanMessage(content=notes),
        ]
    )
    return {"messages": [AIMessage(content=reply.content, name="researcher")]}


def writer(state: State) -> dict:
    reply = llm.invoke(
        [
            SystemMessage(content="你是写手。根据对话里的调研要点写不超过80字的中文短文。"),
            *state["messages"],
        ]
    )
    return {"messages": [AIMessage(content=reply.content, name="writer")]}


def route_next(state: State) -> Literal["researcher", "writer", "__end__"]:
    nxt = state.get("next") or "FINISH"
    if nxt == "researcher":
        return "researcher"
    if nxt == "writer":
        return "writer"
    return "__end__"


builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_edge(START, "supervisor")
builder.add_conditional_edges(
    "supervisor",
    route_next,
    {"researcher": "researcher", "writer": "writer", "__end__": END},
)
builder.add_edge("researcher", "supervisor")
builder.add_edge("writer", "supervisor")
app = builder.compile()

result = app.invoke(
    {
        "messages": [HumanMessage(content="用很短的篇幅介绍 LangGraph 的核心能力。")],
        "next": "",
        "steps": 0,
    }
)
print_messages(result["messages"])
