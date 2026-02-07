from __future__ import annotations
import json
from typing import Any


def canonical_json(obj: Any) -> str:
    """
    Deterministic JSON serialization:
    - sorted keys
    - no insignificant whitespace
    - stable unicode handling
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def canonical_bytes(obj: Any) -> bytes:
    return canonical_json(obj).encode("utf-8")
