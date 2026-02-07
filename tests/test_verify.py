import json
from evidence_ledger_lite import Ledger, LedgerEvent

def test_verify_ok(tmp_path):
    path = tmp_path / "ledger.jsonl"
    ledger = Ledger(path)
    ledger.init()

    ledger.append(LedgerEvent(action="A", entity_type="X", entity_id="1"))
    ledger.append(LedgerEvent(action="B", entity_type="X", entity_id="1"))

    report = ledger.verify()
    assert report["ok"] is True
    assert report["count"] == 2

def test_verify_detects_tamper(tmp_path):
    path = tmp_path / "ledger.jsonl"
    ledger = Ledger(path)
    ledger.init()

    ledger.append(LedgerEvent(action="A", entity_type="X", entity_id="1"))
    ledger.append(LedgerEvent(action="B", entity_type="X", entity_id="1"))

    # Tamper with line 2
    lines = path.read_text(encoding="utf-8").splitlines()
    ev2 = json.loads(lines[1])
    ev2["payload"] = {"tampered": True}
    lines[1] = json.dumps(ev2)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    report = ledger.verify()
    assert report["ok"] is False
    assert any(e["type"] == "HASH_MISMATCH" for e in report["errors"])
