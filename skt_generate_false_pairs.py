#!/usr/bin/env python3
import os, random, shutil

DATA_DIR = "raw_sanskrit_data"
random.seed(42)

files = os.listdir(DATA_DIR)

# Step 1: group all files by base
from collections import defaultdict

base_files = defaultdict(list)
for f in files:
    if f.endswith("_root") or f.endswith("_f"):
        continue  # only care about commentary files for now
    base = f.rsplit("_", 1)[0]
    base_files[base].append(f)

# Step 2: keep only bases that have both a _root and at least one commentary
valid_bases = [
    b for b in base_files
    if f"{b}_root" in files and len(base_files[b]) > 0
]

# Step 3: select one commentary (arbitrary) for each base
p_file = {b: base_files[b][0] for b in valid_bases}  # choose first available

# Step 4: create _f for each base
for base in valid_bases:
    dst = os.path.join(DATA_DIR, f"{base}_f")
    if os.path.exists(dst):
        print(f"Skipping {dst} (already exists)")
        continue

    # pick a different base randomly
    other_base = random.choice([b for b in valid_bases if b != base])
    src = os.path.join(DATA_DIR, p_file[other_base])

    shutil.copyfile(src, dst)
    print(f"Created {dst} ← {src}")
