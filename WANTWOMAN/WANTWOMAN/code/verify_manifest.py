"""Check the delivered WANTWOMAN archive against its SHA-256 manifest."""
from __future__ import annotations
import hashlib
from pathlib import Path
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = root / 'MANIFEST.sha256'
    if not manifest.is_file():
        print('Missing MANIFEST.sha256', file=sys.stderr)
        return 2
    failures = []
    count = 0
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        try:
            expected, relative = line.split('  ', 1)
            path = (root / relative).resolve()
            path.relative_to(root)
        except (ValueError, OSError):
            print(f'Invalid manifest entry: {line!r}', file=sys.stderr)
            return 2
        count += 1
        if not path.is_file():
            failures.append(f'MISSING {relative}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            failures.append(f'MISMATCH {relative}')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'OK: {count} file hashes match.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
