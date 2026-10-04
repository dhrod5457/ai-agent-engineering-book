#!/usr/bin/env python3
"""Verify fixed manuscript bytes and the versioned shared style contract."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[2];folder=Path(__file__).resolve().parent
contract=json.loads((folder/'edition.json').read_text())
for path,sha in contract['manuscript_sha256'].items():
    assert hashlib.sha256((root/path).read_bytes()).hexdigest()==sha, 'Manuscript changed: '+path
for path,sha in contract['style_sha256'].items():
    assert hashlib.sha256((folder/path).read_bytes()).hexdigest()==sha, 'Style changed: '+path
print(contract['version'], 'verified',len(contract['manuscript_sha256']),'manuscript files; shared reader styles valid')
