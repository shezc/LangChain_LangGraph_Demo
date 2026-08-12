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


llm = get_chat_model(temperature=0)

print_divider("LCEL：prompt | model | parser")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "用一句中文回答。"),
        ("human", "{question}"),
    ]
)
chain = prompt | llm | StrOutputParser()
print(chain.invoke({"question": "LCEL 的竖线 | 是什么意思？"}))

print_divider("bind_tools：模型提出调用，本地执行")
llm_with_tools = llm.bind_tools([add])
ai = llm_with_tools.invoke("3 加 19 等于多少？请使用工具计算。")
print("content:", ai.content)
print("tool_calls:", ai.tool_calls)

if ai.tool_calls:
    call = ai.tool_calls[0]
    result = add.invoke(call["args"])
    print("工具返回:", result)
