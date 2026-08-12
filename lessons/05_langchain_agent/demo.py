import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain.agents import create_agent
from langchain_core.tools import tool

from src.common.llm import get_chat_model
from src.common.pretty import print_divider, print_messages


@tool
def get_weather(city: str) -> str:
    """查询城市的模拟天气（教学用，非真实气象）。"""
    demo = {"杭州": "小雨 18°C", "北京": "晴 26°C", "上海": "阴 22°C"}
    return demo.get(city, f"{city}：多云 20°C（模拟数据）")


@tool
def add(a: int, b: int) -> int:
    """两个整数相加。"""
    return a + b


llm = get_chat_model(temperature=0)
agent = create_agent(
    model=llm,
    tools=[get_weather, add],
    system_prompt="你是助手。需要天气或算术时必须调用工具，不要口算或编造天气。",
)

print_divider("Agent 调用")
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "杭州天气怎么样？另外 17 加 25 等于多少？",
            }
        ]
    }
)
print_messages(result["messages"])
