import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain.agents import create_agent
from langchain_core.tools import tool

from src.common.llm import get_chat_model
from src.common.pretty import print_messages


@tool
def get_weather(city: str) -> str:
    """查询城市的模拟天气。"""
    demo = {"杭州": "小雨 18°C", "北京": "晴 26°C", "上海": "阴 22°C"}
    return demo.get(city, f"{city}：多云 20°C（模拟数据）")


@tool
def get_time(city: str) -> str:
    """查询城市的模拟本地时间。"""
    demo = {"杭州": "11:30", "北京": "11:30", "上海": "11:30", "纽约": "23:30"}
    return demo.get(city, f"{city}：09:00（模拟数据）")


agent = create_agent(
    model=get_chat_model(temperature=0),
    tools=[get_weather, get_time],
    system_prompt="需要天气或时间时必须调用工具。用中文简短回答。",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "北京现在几点、天气如何？"}]}
)
print_messages(result["messages"])
