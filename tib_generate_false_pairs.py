#!/usr/bin/env python3
import os, random, shutil, chardet
from collections import defaultdict
from pathlib import Path

DATA_DIR = "raw_tibetan_data"
random.seed(42)                       # reproducible

# ---------- helper: copy & re-encode to UTF-8 --------------------
def copy_as_utf8(src_path: Path, dst_path: Path):
    """Detect the source encoding, decode, and write to dst in UTF-8."""
    raw = src_path.read_bytes()
    det = chardet.detect(raw)
    enc = det["encoding"] or "utf-8"   # fallback, though very rare
    text = raw.decode(enc)             # will raise if truly undecodable
    dst_path.write_text(text, encoding="utf-8")

# ---------- index roots / commentaries ---------------------------
root_files   = {}                 # base → root filename
comm_files   = defaultdict(list)  # base → list[commentary filenames]

for fname in os.listdir(DATA_DIR):
    stem = Path(fname).stem
    if stem.endswith("_root"):
        base = stem.rsplit("_", 1)[0]
        root_files[base] = fname
    elif stem.endswith("_comm"):
        base = stem.rsplit("_", 1)[0]
        comm_files[base].append(fname)

bases = [b for b in root_files if b in comm_files]   # need both root+comm

# ---------- create one negative (_f) per base --------------------
for base in bases:
    neg_fname = f"{base}_f.txt"
    neg_path  = Path(DATA_DIR) / neg_fname

    if neg_path.exists():
        print(f"⏩  Skipping {neg_fname} (already exists)")
        continue

    # pick commentary from a different root
    other_base = random.choice([b for b in bases if b != base])
    src_comm   = random.choice(comm_files[other_base])
    src_path   = Path(DATA_DIR) / src_comm

    copy_as_utf8(src_path, neg_path)
    print(f"✅  Created {neg_fname}  ←  {src_comm}  ({other_base})")

print("Done ✔️")
