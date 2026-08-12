import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from src.common.llm import get_chat_model
from src.common.pretty import print_divider


@tool
def add(a: int, b: int) -> int:
    """把两个整数相加。"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """把两个整数相乘。"""
    return a * b


TOOLS = {"add": add, "multiply": multiply}

llm = get_chat_model(temperature=0)
llm_with_tools = llm.bind_tools([add, multiply])

print_divider("工具调用")
ai = llm_with_tools.invoke("请用工具计算 (6 + 7) * 3。先加法再乘法。")
print("tool_calls:", ai.tool_calls)
for call in ai.tool_calls or []:
    fn = TOOLS[call["name"]]
    value = fn.invoke(call["args"])
    print(f"{call['name']}({call['args']}) -> {value}")

print_divider("LCEL 先译后答")
chain = (
    ChatPromptTemplate.from_messages(
        [
            ("system", "先把问题译成英文，再只用一句中文回答问题本身。"),
            ("human", "{question}"),
        ]
    )
    | llm
    | StrOutputParser()
)
print(chain.invoke({"question": "什么是 tool calling？"}))
