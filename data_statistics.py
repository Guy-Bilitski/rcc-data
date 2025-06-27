#!/usr/bin/env python3
import os
from pathlib import Path

FOLDERS = ["raw_sanskrit_data", "raw_tibetan_data"]

def stats(folder: str):
    files = os.listdir(folder)

    # collect every base that has a _root.<ext>
    root_bases = {
        Path(f).stem.rsplit("_", 1)[0].lower()
        for f in files
        if Path(f).stem.lower().endswith("_root")
    }

    f_bases = {
        Path(f).stem.rsplit("_", 1)[0].lower()
        for f in files
        if Path(f).stem.lower().endswith("_f")
    }

    missing_f = sorted(root_bases - f_bases)
    return len(root_bases), len(missing_f), missing_f

# ---------------- MAIN ----------------
for folder in FOLDERS:
    total, missing, missing_list = stats(folder)
    print(f"{folder}:")
    print(f"  total roots......... {total}")
    print(f"  roots without _f.... {missing}")
    if missing_list:
        print("  missing root bases:")
        for b in missing_list:
            print(f"    - {b}")
    print()
