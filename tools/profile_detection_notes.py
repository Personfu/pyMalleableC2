#!/usr/bin/env python3
"""Extract detection notes from a profile-like text file.

This is defensive analysis only. It does not generate profiles, launch C2, or
provide evasion instructions.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

URI_RE = re.compile(r"/[-A-Za-z0-9_./]{2,}")
HEADER_RE = re.compile(r"(?im)^\s*([A-Za-z0-9-]{3,40})\s*[:=]\s*(.{2,120})$")


def analyze(text: str) -> str:
    uris = sorted(set(URI_RE.findall(text)))[:50]
    headers = sorted(set(f'{k}: {v.strip()}' for k, v in HEADER_RE.findall(text)))[:50]
    lines = ['# Profile Detection Notes', '', '## Candidate URI Patterns', '']
    lines.extend(f'- `{uri}`' for uri in uris) or lines.append('- None observed')
    lines.extend(['', '## Candidate Header Patterns', ''])
    lines.extend(f'- `{header}`' for header in headers) or lines.append('- None observed')
    lines.extend([
        '',
        '## Defensive Use',
        'Convert stable URI/header traits into detection hypotheses, then validate against benign traffic to reduce false positives.',
        '',
    ])
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract defensive detection notes from local text.')
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.write_text(analyze(args.input.read_text(encoding='utf-8', errors='ignore')), encoding='utf-8')
    print(f'wrote {args.output}')


if __name__ == '__main__':
    main()
