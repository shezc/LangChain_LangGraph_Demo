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
    skills: list[str] = Field(description="技能列表")


llm = get_chat_model(temperature=0)
extractor = llm.with_structured_output(Person)
person = extractor.invoke(
    "从文本抽取人物信息：李华今年 28 岁，会 Python 和 SQL，最近在学 LangGraph。"
)
print(person.model_dump_json(indent=2))
