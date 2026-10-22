"""
Copy the reference values used by ``tests/test_goldens.py`` from the TerraME
``sysdyn`` goldens of ``terrame-goldens``.

Every golden is copied as is (``<case>.csv.gz``: a column ``step`` and one per
variable, values with 17 significant digits), except Lorenz (10000 steps),
which keeps steps 0 to 100 and then every 100th step. ``reference.json``
records the source version, the package commits and the SHA-256 of each
source file.

    python tests/goldens/make_reference.py /path/to/terrame-goldens
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def write_gz(text: str, dest: Path) -> None:
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0, compresslevel=9) as gz:
        gz.write(text.encode())
    dest.write_bytes(buf.getvalue())


def main(root: Path) -> None:
    src = root / "goldens" / "sysdyn"
    sources = {}
    for path in sorted(src.glob("*.csv.gz")):
        sources[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        with gzip.open(path, "rt", newline="") as f:
            lines = f.read().splitlines()
        if path.name == "lorenz.csv.gz":
            lines = [lines[0]] + [
                ln for ln in lines[1:]
                if (s := int(ln.split(",", 1)[0])) <= 100 or s % 100 == 0
            ]
        write_gz("\n".join(lines) + "\n", HERE / path.name)
    (HERE / "cases.csv").write_bytes((src / "cases.csv").read_bytes())
    manifest = json.loads((root / "manifest.json").read_text())
    meta = {
        "source": "https://github.com/LambdaGeo/terrame-goldens",
        "version": manifest["version"],
        "terrame": manifest["terrame"],
        "packages": [p for p in manifest["packages"] if p["name"] in ("sysdyn", "sci")],
        "files": sources,
        "lorenz_steps": "0 to 100, then every 100th step",
    }
    (HERE / "reference.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"{len(sources)} goldens copied")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
