from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def require_openrouter_key() -> str:
    load_env()
    key = (os.getenv("OPENROUTER_API_KEY") or "").strip()
    placeholder = key.startswith("sk-or-v1-xxx") or key in {"", "your-key-here"}
    if not key or placeholder:
        print(
            "未检测到有效的 OPENROUTER_API_KEY。\n"
            "请复制 .env.example 为 .env，并填入你的 OpenRouter API Key。\n"
            "获取地址: https://openrouter.ai/keys"
        )
        sys.exit(1)
    return key
