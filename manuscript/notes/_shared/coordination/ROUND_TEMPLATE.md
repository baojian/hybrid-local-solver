# Research round template

Use one file under [`rounds/`](rounds/) for every controller-managed parallel
research cycle. A round record is an evidence index and routing log, not a
substitute for the direction notes or their proofs.

```markdown
# Research round <NNN>: <short theme>

Date: YYYY-MM-DD
Controller snapshot: <branch or dirty-tree description>
Controller family: <family>
Controller branch: `agent/<family>/<task>`
Base commit: `<40-character commit>`
Round state: <active | reviewed | redistributed>

## Assignments

| Direction | Agent family | Branch | Exact target | Allowed edit scope | Outcome |
|---|---|---|---|---|---|
| `<note-id>` | `<family>` | `agent/<family>/<task>` | One falsifiable question | `<note-id>/` | `<pending | proved | conditional | refuted | narrowed | no-change>` |

## Direction handoffs

### `<note-id>`

- Claim-status change:
- Evidence pointer:
- Work/accuracy qualifiers:
- Reusable output:
- Refuted or narrowed route:
- Verification performed:

## Controller adjudication

| Candidate conclusion | Decision | Exact evidence checked | Shared destination |
|---|---|---|---|
| ... | `<promote | direction-local | reject | needs-review>` | ... | ... |

## Redistribution messages

| Finding | Recipient directions | Required action |
|---|---|---|
| ... | ... | ... |

## Metadata and shared-state changes

- Results ledger:
- Broadcast:
- Related work:
- Taxonomy/dependencies:
- Manifest/index:

## Validation

- Direction builds:
- `make note-audit`:
- Focused/full tests:
- Lint and diff checks:
- Concurrent-work caveats:

## Next round queue

1. One precise next target.
```

The controller changes `Round state` to `reviewed` only after checking the
named evidence, and to `redistributed` only after the shared broadcast and all
affected direction handoffs agree.
