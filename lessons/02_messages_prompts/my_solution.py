import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)


from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from src.common.llm import get_chat_model
from src.common.pretty import print_divider, print_messages


llm = get_chat_model(temperature=0)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是翻译器，将{source_lang}翻译为{target_lang}。"),
        ("human", "{text}"),
    ]
)

chain_input = {
    "source_lang": "中文",
    "target_lang": "英文",
    "text": "LangGraph 用图来编排 Agent",
}
# 用变量填充prompt模板
prompted = prompt.invoke(chain_input)
llm_response = llm.invoke(prompted)
print(llm_response.content)


# 多轮对话
messages = [HumanMessage(content="用一个词概括 Langgraph")]

messages.append(AIMessage(content=llm.invoke(messages).content))
messages.append(HumanMessage(content="为什么是这个词？"))

result = llm.invoke(messages)
print_divider("多轮对话")
print(result.content)
print_messages([*messages, result])
