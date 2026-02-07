from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class LedgerEvent:
    """
    A single append-only event in a tamper-evident chain.
    Keep payload small; prefer hashes for large artifacts.
    """
    action: str
    entity_type: str
    entity_id: str
    actor: str = "system"
    payload: Dict[str, Any] = field(default_factory=dict)
    evidence_refs: List[Dict[str, Any]] = field(default_factory=list)

    # System fields
    ts: str = field(default_factory=utc_now_iso)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prev_hash: Optional[str] = None
    hash: Optional[str] = None  # computed at append time

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "ts": self.ts,
            "actor": self.actor,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "payload": self.payload,
            "evidence_refs": self.evidence_refs,
            "prev_hash": self.prev_hash,
            "hash": self.hash,
        }

    def content_to_hash(self) -> Dict[str, Any]:
        """
        The hash should NOT include the hash field itself.
        It should include prev_hash to chain the log.
        """
        d = self.to_dict().copy()
        d["hash"] = None
        return d
