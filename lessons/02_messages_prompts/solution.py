import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from src.common.llm import get_chat_model
from src.common.pretty import print_divider

llm = get_chat_model(temperature=0)

print_divider("翻译模板")
translator = ChatPromptTemplate.from_messages(
    [
        ("system", "你是翻译器。把用户文本从{source_lang}译成{target_lang}，只输出译文。"),
        ("human", "{text}"),
    ]
)
messages = translator.invoke(
    {
        "source_lang": "中文",
        "target_lang": "英文",
        "text": "LangGraph 用图来编排 Agent",
    }
)
translation = llm.invoke(messages)
print(translation.content)

print_divider("多轮追问")   
history = [
    SystemMessage(content="用中文简短回答。"),
    HumanMessage(content="用一个词概括 LangGraph。"),
]
first = llm.invoke(history)
history.extend([first, HumanMessage(content="为什么是这个词？")])
second = llm.invoke(history)
print("第一轮:", first.content)
print("第二轮:", second.content)
