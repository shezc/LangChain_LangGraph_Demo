import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from src.common.llm import get_chat_model
from src.common.pretty import print_divider, print_messages

llm = get_chat_model(temperature=0)

print_divider("多轮消息")
messages = [
    SystemMessage(content="你是简洁的助手，用中文回答，不超过两句。"),
    HumanMessage(content="什么是 token？"),
    AIMessage(content="Token 是模型读写文本时切分出的小片段。"),
    HumanMessage(content="那上下文窗口又是什么？"),
]
response = llm.invoke(messages)
print_messages([*messages, response])

print_divider("ChatPromptTemplate")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是{role}，用{style}风格回答。"),
        ("human", "{question}"),
    ]
)
chain_input = {
    "role": "编程导师",
    "style": "短句、举例",
    "question": "什么是 LCEL？",
}
prompted = prompt.invoke(chain_input)
print(prompted.to_string())
print("模型回复:", llm.invoke(prompted).content)
