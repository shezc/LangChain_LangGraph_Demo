from __future__ import annotations

import sys
from pathlib import Path


def bootstrap(file: str, parents: int = 2) -> Path:
    """Put the repo root on sys.path so `from src.common ...` works."""
    root = Path(file).resolve().parents[parents]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    return root
