#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
repo=Path(__file__).resolve().parents[2];publisher=repo.parent/'published-book'
subprocess.run([sys.executable,str(publisher/'scripts/build_common_books.py'),repo.name],check=True)
