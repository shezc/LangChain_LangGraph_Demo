from __future__ import annotations

from typing import Any


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def message_text(message: Any) -> str:
    content = getattr(message, "content", message)
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                parts.append(str(block["text"]))
            else:
                parts.append(str(block))
        return "".join(parts)
    return str(content)


def print_messages(messages: list[Any]) -> None:
    for message in messages:
        role = getattr(message, "type", None) or message.__class__.__name__
        name = getattr(message, "name", None)
        label = f"{role}/{name}" if name else str(role)
        tool_calls = getattr(message, "tool_calls", None)
        print(f"[{label}] {message_text(message)}")
        if tool_calls:
            print(f"  tool_calls: {tool_calls}")
