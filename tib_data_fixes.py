#!/usr/bin/env python3
"""
tib_fix_all_filenames.py
---------------------------------
Goal: in `raw_tibetan_data/` make **every** text file conform to
    <base>_(root|comm).txt   or   <base>_f.txt

Problems handled
----------------
1. **Sub‑folders named *_Root / *_Comm** – files inside often lack the
   suffix or have it after the extension.  We rename them _in place_.

2. **Top‑level stray files** such as
       "SN 1 Root.txt", "SN 1 Comm..txt",  "SN 8 Comm.",
       "Viṃśikā 10 Root (Du).txt" …
   We normalise these to *_root.txt / *_comm.txt*.

3. **Suffix after .txt** (e.g. `D3871_0.txt_root.txt`) is fixed.

4. **Duplicate targets** – if renaming would overwrite an existing file,
   we append `_1`, `_2`, … to keep everything.

The script does **not flatten** directories; it only renames.
If you later want everything flat, run your existing flattener afterwards.
"""

import os, re
from pathlib import Path
from typing import Optional
import shutil

DATA_DIR = Path("raw_tibetan_data")
SUFFIXES  = {"root": "_root.txt", "comm": "_comm.txt"}

# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------

def ensure_suffix(fname: str, suffix_word: str) -> str:
    """Return filename that ends with _root.txt or _comm.txt (lower‑case)."""
    suffix = SUFFIXES[suffix_word]

    # already correct
    if fname.lower().endswith(suffix):
        return fname

    stem, ext = os.path.splitext(fname)
    if ext.lower() == ".txt":                       # insert before .txt
        return f"{stem}{suffix}"
    return f"{fname}{suffix}"                         # no extension


def unique_name(p: Path) -> Path:
    """If *p* already exists, append _1, _2 … until unique."""
    if not p.exists():
        return p
    stem, ext = p.stem, p.suffix
    idx = 1
    while True:
        candidate = p.with_name(f"{stem}_{idx}{ext}")
        if not candidate.exists():
            return candidate
        idx += 1

# ---------------------------------------------------------------------
# Phase A – handle *_Root / *_Comm sub‑folders
# ---------------------------------------------------------------------

def rename_inside_folder(folder: Path, suffix_word: str):
    for f in folder.iterdir():
        if not f.is_file():
            continue
        new_name = ensure_suffix(f.name, suffix_word)
        if new_name == f.name:
            continue
        target = unique_name(f.with_name(new_name))
        f.rename(target)
        print(f"   • {f.relative_to(DATA_DIR)}  →  {target.name}")

for sub in DATA_DIR.iterdir():
    if not sub.is_dir():
        continue
    name_lower = sub.name.lower()
    if name_lower.endswith("_root"):
        print(f"\n📂 Fixing files in folder {sub.name}")
        rename_inside_folder(sub, "root")
    elif name_lower.endswith("_comm"):
        print(f"\n📂 Fixing files in folder {sub.name}")
        rename_inside_folder(sub, "comm")

# ---------------------------------------------------------------------
# Phase B – Make two pairs for the same root in Viṃśikā + Vṛtti Tib folder
# ---------------------------------------------------------------------
folder = "raw_tibetan_data/Viṃśikā + Vṛtti Tib"
for filename in os.listdir(folder):
    src = os.path.join(folder, filename)

    # Rename: move "(Du)" before "Root"
    if "Root (Du)" in filename:
        new_name = filename.replace("Root (Du)", "Du Root")
        dst = os.path.join(folder, new_name)
        os.rename(src, dst)
        print(f"Renamed: {filename} → {new_name}")

    # Duplicate: make "Du Comm" copy of each "Comm"
    elif "Comm" in filename and "Du" not in filename:
        base, ext = os.path.splitext(filename)
        new_name = filename.replace("Comm", "Du Comm")
        src_path = os.path.join(folder, filename)
        dst_path = os.path.join(folder, new_name)

        shutil.copyfile(src_path, dst_path)
        print(f"Duplicated: {filename} → {new_name}")

# ---------------------------------------------------------------------
# Phase C – fix stray top‑level files (and any files nested deeper)
# ---------------------------------------------------------------------
# Regex captures <base> + root/comm even with spaces, dots, () etc.
FIX_RX = re.compile(
    r"^(.*?)\s*(root|comm)\b.*$",
    re.I,
)

# Accept target pattern (already valid)
VALID_RX = re.compile(r".+_(root|comm|f)\.txt$", re.I)

def fix_file(path: Path):
    if VALID_RX.match(path.name):
        return False

    m = FIX_RX.match(path.stem)
    if not m:
        return False  # can't fix automatically

    base_raw, suf_word = m.groups()
    suffix_word = suf_word.lower()

    # Normalise base: collapse whitespace to '_', strip outer spaces/dots
    base_norm = re.sub(r"\s+", "_", base_raw.strip(" ._"))
    new_name  = f"{base_norm}{SUFFIXES[suffix_word]}"

    target = unique_name(path.with_name(new_name))
    path.rename(target)
    print(f"✅ {path.relative_to(DATA_DIR)} → {target.name}")
    return True

print("\n📑 Scanning for stray filenames …")
changes = 0
for p in DATA_DIR.rglob("*.txt"):
    if fix_file(p):
        changes += 1

print(f"\n✔️  Renaming complete.  {changes} file(s) fixed.")
