# Readable original research records

These are 1,010 text files extracted from four original deterministic research archives during public-release preparation on September 14, 2026. Every exported file preserves the original member's exact content bytes. `MANIFEST.json` records each archive's original path and SHA-256, each member's path and checksum, and the explicit omissions.

The records retain earlier failed, open, corrected, and final attempts. A statement in an old STATUS file is historical, not the current theorem status. Read the active manuscript and the standalone notes for the reconciled claims.

- `deterministic-audit-portable/`: portable solver, tests, proof-to-code explanation, and proof audit source.
- `deterministic-audit-research/`: original audit/refinement notes, programs, and handoffs.
- `deterministic-proof-portable/`: original deterministic proof and portable implementation records.
- `deterministic-proof-research/`: working notes, proof attempts, programs, and measurements from the substantive research archive.

Source/executable filenames such as `.py`, `.tex`, and `.sh` receive an additional `.txt` suffix for browsing. This keeps these historical standalone snapshots outside the current project's build/test discovery. Their contents have not been edited. Text notes and data retain their ordinary extensions. Nested archives, compiled binaries, environments, logs, build artifacts, and unsupported formats are omitted as listed in the manifest. The original bundles remain private.

To reconstruct one excerpt in a new directory, run the following from the repository root, replacing the example ID and destination as needed. This only copies the exported text and does not execute archived programs:

```python
from pathlib import Path
import hashlib
import json

source = Path("manuscript/research-records").resolve()
destination = Path("tmp/deterministic-audit-portable").resolve()
manifest = json.loads((source / "MANIFEST.json").read_text())
record = next(x for x in manifest["archives"] if x["id"] == "deterministic-audit-portable")
for item in record["files"]:
    original = (source / item["exported_path"]).resolve()
    target = (destination / item["member"]).resolve()
    assert original.is_relative_to(source) and target.is_relative_to(destination)
    data = original.read_bytes()
    assert hashlib.sha256(data).hexdigest() == item["sha256"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
```

The reconstruction is an explicitly incomplete excerpt when the manifest lists omitted files. An original package's own manifest can consequently reference files that are intentionally absent. Use this public export manifest to distinguish those omissions from corruption. The extracted snapshots are reference evidence; maintained solver interfaces remain under `src/`.
