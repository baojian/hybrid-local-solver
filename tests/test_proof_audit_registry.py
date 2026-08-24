from experiments.proof_audits.runner import audit_registry, load_audits


def test_proof_audit_registry_matches_disk() -> None:
    assert audit_registry() == []


def test_each_audited_note_has_a_fast_representative() -> None:
    audits = load_audits()
    audited_notes = {audit.note for audit in audits}
    fast_notes = {audit.note for audit in audits if audit.fast}
    assert fast_notes == audited_notes


def test_audit_ids_are_mechanism_based() -> None:
    for audit in load_audits():
        mechanism = audit.id.split(".", maxsplit=1)[1]
        assert not mechanism.startswith("round")
        assert f"/{mechanism}.py" in audit.script
