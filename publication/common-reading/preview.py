#!/usr/bin/env python3
"""Build a local reading preview from the pinned published edition, not the manuscript."""
from pathlib import Path
import subprocess,sys
repo=Path(__file__).resolve().parents[2]
publisher=repo.parent/'published-book'
if not (publisher/'scripts/restyle_books.py').exists():
    raise SystemExit('Place published-book common-reading checkout next to this repository.')
subprocess.run([sys.executable,str(publisher/'scripts/restyle_books.py'),repo.name],check=True)
subprocess.run(['node',str(publisher/'scripts/build_reading_pdf.cjs'),repo.name],check=True)
