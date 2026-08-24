# Direction handoff template

Copy this structure into the direction's `STATUS.md` or use it in the message
returned to the controller.

```markdown
# Direction status: <note-id>

Last reviewed: YYYY-MM-DD
State: <source | proved-open | conditional | measured | synthesis | refuted>

Choose exactly one state value from the enum above; put qualifications in the
claim ledger rather than appending prose to `State`.

## Exact question and contract

- **Question:**
- **Model:**
- **Accuracy namespace:**
- **Access and charged work:**
- **Intended result:**

## Claim ledger

- **Source:**
- **Proved here:**
- **Conditional:**
- **Measured:**
- **Refuted:**
- **Open:**

## Central blocker

One falsifiable missing lemma, counterexample search, implementation interface,
or experiment.

## Dependencies and reusable outputs

- Formal registry dependencies:
- Source/shared prerequisites:
- Context/provenance:
- Supplies to:

## Resume here

- Exact file/section/lemma:
- Next concrete action:
- Stop/go test:

## Verification

- Source pointers checked:
- Focused build/checks run:
- Known gaps:
```

Keep the status concise. Long derivations and experiment records belong in the
direction note or the appropriate code/experiment area. Prefer stable LaTeX
labels, section names, equation names, test names, or source anchors over bare
line ranges; line numbers drift as parallel work grows the note.
