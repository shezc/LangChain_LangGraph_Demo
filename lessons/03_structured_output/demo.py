import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from pydantic import BaseModel, Field

from src.common.llm import get_chat_model
from src.common.pretty import print_divider

class Ticket(BaseModel):
    """客服工单摘要。"""

    category: str = Field(description="类别：billing / bug / howto / other")
    urgency: int = Field(description="紧急程度 1-5，5 最紧急")
    summary: str = Field(description="一句话摘要")


llm = get_chat_model(temperature=0)
extractor = llm.with_structured_output(Ticket)

text = "我昨天付了会员费，但账号还是提示未开通，很急，今天要用。"
ticket = extractor.invoke(f"从下面文本抽取工单：\n{text}")

print_divider("结构化结果")
print(ticket.model_dump_json(indent=2))
print("类型:", type(ticket).__name__)
