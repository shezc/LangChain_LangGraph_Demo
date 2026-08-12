import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from src.common.llm import get_chat_model
from src.common.pretty import print_divider

prompt = "写一个关于猫咪的短句。"
strict = get_chat_model(temperature=0)
creative = get_chat_model(temperature=1.2)

print_divider("temperature=0")
print(strict.invoke(prompt).content)

print_divider("temperature=1.2")
print(creative.invoke(prompt).content)

print_divider("stream 小诗")
for chunk in creative.stream("写一首四行小诗，主题是雨天的书店。"):
    print(chunk.content, end="", flush=True)
print()
