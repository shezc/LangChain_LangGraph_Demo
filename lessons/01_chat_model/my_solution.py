import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from src.common.llm import get_chat_model
from src.common.pretty import print_divider

llm_0 = get_chat_model(temperature=0)
llm_1_2 = get_chat_model(temperature=1.2)
cat_prompt = "写一个关于猫咪的短句"
poetry_prompt = "写一首关于猫咪的四行小诗"

print_divider("temperature=0 时的返回结果")
llm_0_response = llm_0.invoke(cat_prompt)
print(llm_0_response.content)

print_divider("temperature=1.2 时的返回结果")
llm_1_2_response = llm_1_2.invoke(cat_prompt)
print(llm_1_2_response.content)

print_divider("四行小诗")
for chunk in llm_0.stream(poetry_prompt):
    print(chunk.content,end="", flush=True)
print()

print_divider("四行小诗")
for chunk in llm_1_2.stream(poetry_prompt):
    print(chunk.content,end="", flush=True)
print()
