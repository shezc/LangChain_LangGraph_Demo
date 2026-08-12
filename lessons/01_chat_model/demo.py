import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from src.common.llm import get_chat_model
from src.common.pretty import print_divider

llm = get_chat_model(temperature=0.2)

print_divider("invoke：一次返回完整回复")
response = llm.invoke("用一句话介绍 LangChain。")
print(response.content)

print_divider("stream：逐块打印")
for chunk in llm.stream("用两句话说明 LangGraph 和 LangChain 的关系。"):
    print(chunk.content, end="", flush=True)
print()
