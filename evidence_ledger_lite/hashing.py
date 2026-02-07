from __future__ import annotations
import hashlib
from typing import Optional


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def chain_hash(prev_hash: Optional[str], event_hash: str) -> str:
    """
    Optional helper if you ever want a second-level hash.
    v0.1 uses prev_hash stored on event + event.hash computed from event content.
    """
    prev = prev_hash or ""
    return sha256_hex((prev + event_hash).encode("utf-8"))
