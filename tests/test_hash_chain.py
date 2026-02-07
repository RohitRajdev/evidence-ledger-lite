from evidence_ledger_lite import Ledger, LedgerEvent

def test_hash_chain(tmp_path):
    path = tmp_path / "ledger.jsonl"
    ledger = Ledger(path)
    ledger.init()

    e1 = ledger.append(LedgerEvent(action="A", entity_type="X", entity_id="1"))
    e2 = ledger.append(LedgerEvent(action="B", entity_type="X", entity_id="1"))

    assert e2.prev_hash == e1.hash
