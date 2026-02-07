from __future__ import annotations
import argparse
import json
from pathlib import Path

from .ledger import Ledger
from .models import LedgerEvent


def cmd_init(args: argparse.Namespace) -> int:
    Ledger(args.ledger).init(overwrite=args.overwrite)
    print(f"Initialized ledger: {args.ledger}")
    return 0


def cmd_append(args: argparse.Namespace) -> int:
    ledger = Ledger(args.ledger)
    payload = json.loads(Path(args.event).read_text(encoding="utf-8"))

    # Accept either a raw event dict or a minimal shape
    # Minimal shape required: action, entity_type, entity_id
    ev = LedgerEvent(
        action=payload["action"],
        entity_type=payload["entity_type"],
        entity_id=payload["entity_id"],
        actor=payload.get("actor", "cli"),
        payload=payload.get("payload", {}),
        evidence_refs=payload.get("evidence_refs", []),
    )

    appended = ledger.append(ev)
    print(json.dumps(appended.to_dict(), indent=2, ensure_ascii=False))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    report = Ledger(args.ledger).verify()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 2


def main() -> int:
    parser = argparse.ArgumentParser(prog="evidence-ledger", description="Tamper-evident JSONL audit ledger.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Initialize an empty ledger file.")
    p_init.add_argument("ledger", help="Path to ledger JSONL file.")
    p_init.add_argument("--overwrite", action="store_true", help="Overwrite if file exists.")
    p_init.set_defaults(func=cmd_init)

    p_append = sub.add_parser("append", help="Append an event from a JSON file.")
    p_append.add_argument("ledger", help="Path to ledger JSONL file.")
    p_append.add_argument("--event", required=True, help="Path to event JSON.")
    p_append.set_defaults(func=cmd_append)

    p_verify = sub.add_parser("verify", help="Verify ledger integrity.")
    p_verify.add_argument("ledger", help="Path to ledger JSONL file.")
    p_verify.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
