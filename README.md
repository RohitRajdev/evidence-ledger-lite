#evidence-ledger-lite
Append-only, hash-chained evidence logs for analytics &amp; AI pipelines.


## Why
Evidence artifacts and decision logs are easy to modify after the fact.  
This library provides a small, deterministic, tamper-evident JSONL ledger.

## Features
- Append-only JSONL ledger
- Deterministic canonical hashing (SHA-256)
- Hash chain via `prev_hash`
- End-to-end verification

## Install (local dev)
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -e .[dev]

Quickstart
  evidence-ledger init demo_ledger.jsonl
  evidence-ledger append demo_ledger.jsonl --event examples/sample_event.json
  evidence-ledger verify demo_ledger.jsonl

Python usage
  from evidence_ledger_lite import Ledger, LedgerEvent

  ledger = Ledger("audit.jsonl")
  ledger.init()

  ledger.append(LedgerEvent(
    actor="service",
    action="INGEST_PUBLIC_SIGNAL",
    entity_type="SKU",
    entity_id="ABC",
    payload={"payload_hash": "sha256:..."}
  ))

print(ledger.verify())

Threat model (honest)

Protects against:

  Silent modifications to past events

  Undetected deletion/insertion of events

Does not protect against:

  Deleting the entire ledger file (store it durably)

  Compromised runtime that writes false events

  Key management / signatures (future extension)
