from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable, List, Optional, Union

from .canonical import canonical_bytes
from .hashing import sha256_hex
from .models import LedgerEvent


PathLike = Union[str, Path]


class Ledger:
    """
    JSONL-backed append-only ledger.
    Each line is a complete event dict.
    """
    def __init__(self, path: PathLike):
        self.path = Path(path)

    def init(self, overwrite: bool = False) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists() and not overwrite:
            return
        self.path.write_text("", encoding="utf-8")

    def _read_events(self) -> List[dict]:
        if not self.path.exists():
            return []
        lines = [ln.strip() for ln in self.path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        events = []
        for ln in lines:
            events.append(json.loads(ln))
        return events

    def last_hash(self) -> Optional[str]:
        events = self._read_events()
        if not events:
            return None
        return events[-1].get("hash")

    def append(self, event: LedgerEvent) -> LedgerEvent:
        self.init(overwrite=False)

        prev = self.last_hash()
        event.prev_hash = prev

        # compute hash of canonicalized content
        event.hash = sha256_hex(canonical_bytes(event.content_to_hash()))

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")

        return event

    def append_many(self, events: Iterable[LedgerEvent]) -> List[LedgerEvent]:
        out: List[LedgerEvent] = []
        for e in events:
            out.append(self.append(e))
        return out

    def verify(self) -> dict:
        """
        Verifies:
        1) hash correctness for each event
        2) prev_hash chaining correctness
        Returns a report dict.
        """
        events = self._read_events()
        if not events:
            return {"ok": True, "count": 0, "head": None, "tail": None, "errors": []}

        errors = []
        prev_hash = None

        for idx, e in enumerate(events):
            got_prev = e.get("prev_hash")
            got_hash = e.get("hash")

            # Check chain pointer
            if got_prev != prev_hash:
                errors.append({
                    "index": idx,
                    "type": "CHAIN_MISMATCH",
                    "expected_prev_hash": prev_hash,
                    "got_prev_hash": got_prev
                })

            # Recompute hash
            content = dict(e)
            content["hash"] = None
            expected_hash = sha256_hex(canonical_bytes(content))
            if got_hash != expected_hash:
                errors.append({
                    "index": idx,
                    "type": "HASH_MISMATCH",
                    "expected_hash": expected_hash,
                    "got_hash": got_hash
                })

            prev_hash = got_hash

        return {
            "ok": len(errors) == 0,
            "count": len(events),
            "head": events[0].get("hash"),
            "tail": events[-1].get("hash"),
            "errors": errors,
        }
