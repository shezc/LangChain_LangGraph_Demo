import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.common.script import bootstrap

bootstrap(__file__)


from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.common.llm import get_chat_model, get_embeddings
from src.common.pretty import print_divider


corpus_path = Path(__file__).with_name("corpus") / "demo.txt"
raw = corpus_path.read_text(encoding="utf-8")

splitter = RecursiveCharacterTextSplitter(chunk_size=180,chunk_overlap = 40)
docs = splitter.create_documents([raw])

store = InMemoryVectorStore.from_documents(docs, get_embeddings())
retriever = store.as_retriever(search_kwargs={"k": 2})

question = "胡婷的爸爸叫什么"

hits: list[Document] = retriever.invoke(question)

print_divider("检索到的片段")
for i, doc in enumerate(hits, 1):
    print(f"[{i}] {doc.page_content}\n")

prompt= ChatPromptTemplate.from_messages(
  [
    (
      "system","只根据提供的资料回答问题，如果资料里没有，就回答不知道。\n\n资料：\n{context}"
    ),
    (
      "human",
      "{question}"
    )
  ]
)

context = "\n\n".join(doc.page_content for doc in hits)
llm = get_chat_model(temperature=0)
answer = (prompt | llm).invoke({
  "context": context,
  "question": question
})
print_divider("RAG 回答")
print(answer.content)


