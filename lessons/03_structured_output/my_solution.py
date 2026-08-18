import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from pydantic import BaseModel, Field

from src.common.llm import get_chat_model


class Person(BaseModel):
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    skills: list[str] = Field(description="掌握的技能")


llm = get_chat_model(temperature=0)

extractor = llm.with_structured_output(Person)

text = "李华今年28岁，会Python 和 SQL，最近在学Langgraph"
llm_response = extractor.invoke(f"从下面文本中提取人物信息, \n{text}")

# print(llm_response)
print(llm_response.model_dump_json(indent=2))
