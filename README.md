# evidence-ledger-lite
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
