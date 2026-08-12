import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.common.llm import get_chat_model, get_embeddings
from src.common.pretty import print_divider

base = (Path(__file__).with_name("corpus") / "langchain_intro.txt").read_text(
    encoding="utf-8"
)
extra = "本仓库的 capstone 模块编号是 12，主题是带记忆、工具和人工确认的小助手。"
splitter = RecursiveCharacterTextSplitter(chunk_size=180, chunk_overlap=40)
docs = splitter.create_documents([base, extra])
store = InMemoryVectorStore.from_documents(docs, get_embeddings())

question = "这个学习仓库的 capstone 模块编号是多少？"
hits = store.as_retriever(search_kwargs={"k": 3}).invoke(question)

print_divider("命中片段")
for i, doc in enumerate(hits, 1):
    print(f"[{i}] {doc.page_content}\n")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "只根据资料回答。资料：\n{context}"),
        ("human", "{question}"),
    ]
)
context = "\n\n".join(doc.page_content for doc in hits)
answer = (prompt | get_chat_model(temperature=0)).invoke(
    {"context": context, "question": question}
)
print_divider("回答")
print(answer.content)
