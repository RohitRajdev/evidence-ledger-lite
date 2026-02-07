from evidence_ledger_lite.canonical import canonical_json

def test_canonical_is_deterministic():
    a = {"b": 1, "a": 2}
    b = {"a": 2, "b": 1}
    assert canonical_json(a) == canonical_json(b)
