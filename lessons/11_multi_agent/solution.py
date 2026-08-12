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
    next: Literal["researcher", "writer", "critic", "FINISH"]


@tool
def search(query: str) -> str:
    """模拟搜索。"""
    return (
        f"关于「{query}」：LangGraph 编排有状态 Agent；"
        "记忆靠 checkpointer；敏感操作靠 interrupt。"
    )


llm = get_chat_model(temperature=0)
router_llm = llm.with_structured_output(Route)


def named(role: str, text: str) -> AIMessage:
    return AIMessage(content=text, name=role)


def supervisor(state: State) -> dict:
    steps = int(state.get("steps") or 0) + 1
    if steps >= 6:
        return {"next": "FINISH", "steps": steps}
    route = router_llm.invoke(
        [
            SystemMessage(
                content=(
                    "调度规则：无调研→researcher；有调研无正文→writer；"
                    "有正文无审稿→critic；审稿已出现→FINISH。"
                )
            ),
            *state["messages"],
        ]
    )
    return {"next": route.next, "steps": steps}


def researcher(state: State) -> dict:
    notes = search.invoke(str(state["messages"][0].content))
    reply = llm.invoke(
        [
            SystemMessage(content="你是研究员，列出3条中文要点。"),
            HumanMessage(content=notes),
        ]
    )
    return {"messages": [named("researcher", reply.content)]}


def writer(state: State) -> dict:
    reply = llm.invoke(
        [
            SystemMessage(content="你是写手，根据要点写不超过80字中文短文。"),
            *state["messages"],
        ]
    )
    return {"messages": [named("writer", reply.content)]}


def critic(state: State) -> dict:
    reply = llm.invoke(
        [
            SystemMessage(content="你是审稿人。用两三句中文点评短文，最后给通过或不通过。"),
            *state["messages"],
        ]
    )
    return {"messages": [named("critic", reply.content)]}


def route_next(state: State) -> str:
    mapping = {
        "researcher": "researcher",
        "writer": "writer",
        "critic": "critic",
        "FINISH": "__end__",
    }
    return mapping.get(state.get("next") or "FINISH", "__end__")


builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("critic", critic)
builder.add_edge(START, "supervisor")
builder.add_conditional_edges(
    "supervisor",
    route_next,
    {
        "researcher": "researcher",
        "writer": "writer",
        "critic": "critic",
        "__end__": END,
    },
)
builder.add_edge("researcher", "supervisor")
builder.add_edge("writer", "supervisor")
builder.add_edge("critic", "supervisor")
app = builder.compile()

result = app.invoke(
    {
        "messages": [HumanMessage(content="介绍 LangGraph 核心能力。")],
        "next": "",
        "steps": 0,
    }
)
print_messages(result["messages"])
