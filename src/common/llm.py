from __future__ import annotations

import hashlib
import math
import os

from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI

from src.common.env import load_env, require_openrouter_key

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def get_chat_model(temperature: float = 0.2, **kwargs) -> ChatOpenAI:
    """Create a chat model that talks to OpenRouter (OpenAI-compatible)."""
    api_key = require_openrouter_key()
    load_env()
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
        temperature=temperature,
        default_headers={
            "HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost"),
            "X-Title": os.getenv("OPENROUTER_APP_TITLE", "LangChain LangGraph Demo"),
        },
        **kwargs,
    )


class HashingEmbeddings(Embeddings):
    """Deterministic bag-of-tokens embeddings for local RAG demos.

    Production apps should use a real embedding model. This helper lets the
    RAG lesson run without a second paid API.
    """

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def _embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        for token in text.lower().replace("\n", " ").split():
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            vec[int(digest, 16) % self.dim] += 1.0
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


def get_embeddings() -> Embeddings:
    return HashingEmbeddings()
