from evidence_ledger_lite import Ledger, LedgerEvent

ledger = Ledger("kartjourney_audit.jsonl")
ledger.init()

# Log a governance event (safe: metadata + hashes, not proprietary logic)
evt = LedgerEvent(
    actor="kartjourney",
    action="INGEST_PUBLIC_SIGNAL",
    entity_type="SKU",
    entity_id="SANRIO-123",
    payload={
        "signal_source": "public_shopper_signal",
        "signal_ts": "2026-02-07T12:00:00Z",
        "payload_hash": "sha256:...hash-of-raw-signal-json...",
    },
    evidence_refs=[
        {"type": "url", "value": "https://www.example.com/product/xyz", "captured_at": "2026-02-07T12:00:00Z"}
    ],
)

ledger.append(evt)

print(ledger.verify())
