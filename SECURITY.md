# Security Policy

If you discover a security issue, please open a private report or email the maintainer.
This project is a lightweight integrity tool and does not manage secrets by default.


Quick run commands


python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

pytest -q

evidence-ledger init demo.jsonl
evidence-ledger append demo.jsonl --event examples/sample_event.json
evidence-ledger verify demo.jsonl
