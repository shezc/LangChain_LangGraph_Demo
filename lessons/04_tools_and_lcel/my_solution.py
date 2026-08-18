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
def multiply(a: int, b: int) -> int:
    """将两数相乘"""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """将两数相加"""
    return a + b


llm = get_chat_model(temperature=1)

prompt = ChatPromptTemplate.from_messages(
    [("system", "请用工具计算"), ("human", "{question}")]
)

chain = prompt | llm | StrOutputParser()
question = "(6+7)*3等于多少?"

chain_response = chain.invoke({"question": question})
print_divider("chain_response的结果为")
print(chain_response)

llm_with_tools = llm.bind_tools([multiply, add])
tools_response = llm_with_tools.invoke(f"{question}请使用工具计算")
print_divider("tools_response的结果为")
print(tools_response.content)

print_divider("tool_calls的第一次结果为")
print(tools_response.tool_calls)


chain_translate = (
    ChatPromptTemplate(
        [
            ("system", "将用户问题翻译为英文后再交给模型使用英文回答"),
            ("human", "{question}"),
        ]
    )
    | llm
    | StrOutputParser()
)

translate_response = chain_translate.invoke(
    {"question": "现在地表最强的llm是哪个，直接告诉我名称即可"}
)
print_divider("translate_response的结果为")
print(translate_response)
