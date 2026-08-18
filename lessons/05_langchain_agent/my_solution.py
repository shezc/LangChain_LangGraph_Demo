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
def get_time(city: str) -> str:
    """查询城市的模拟时间（教学用，非真实时间）。"""
    demo = {"西安": "10:00", "上海": "18:00"}
    return demo.get(city)


@tool
def get_weather(city: str) -> str:
    """查询城市的模拟天气（教学用，非真实天气）。"""
    demo = {"杭州": "小雨 18°C", "北京": "晴 26°C", "上海": "阴 22°C"}
    return demo.get(city)


llm = get_chat_model(temperature=0)
agent = create_agent(
    model=llm,
    tools=[get_time, get_weather],
    system_prompt="你是助手，需要天气和时间时必须调用工具，不要编造天气和时间",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "西安现在是几点？杭州今天天气怎么样"}]}
)

print_divider("Agent 调用")
print_messages(result["messages"])
