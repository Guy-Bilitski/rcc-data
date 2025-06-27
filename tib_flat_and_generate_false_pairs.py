import os, random, shutil
from collections import defaultdict

DATA_DIR = "raw_tibetan_data"           # main folder
random.seed(42)                         # reproducible negatives

# --------------------------------------------------------------------
# 1)  FLATTEN THE TREE  ------------------------------------------------
# --------------------------------------------------------------------
for entry in os.scandir(DATA_DIR):
    if entry.is_dir():
        subdir = entry.path
        for item in os.scandir(subdir):
            src = item.path
            dst = os.path.join(DATA_DIR, item.name)

            # avoid name clashes if the same file name already exists
            if os.path.exists(dst):
                name, ext = os.path.splitext(item.name)
                dst = os.path.join(DATA_DIR, f"{entry.name}_{name}{ext}")

            shutil.move(src, dst)
        # remove the now-empty sub-folder
        os.rmdir(subdir)

print("✔️  All files flattened into", DATA_DIR)

# --------------------------------------------------------------------
# 2)  INDEX ROOT & COMMENTARY FILES  ----------------------------------
# --------------------------------------------------------------------
root_files = {}                 # base → <base>_root.txt
comm_files = defaultdict(list)  # base → [all its commentary files]

for fname in os.listdir(DATA_DIR):
    low = fname.lower()
    if low.endswith("_root.txt"):
        base = fname.rsplit("_", 1)[0]
        root_files[base] = fname
    elif low.endswith("_comm.txt"):
        base = fname.rsplit("_", 1)[0]
        comm_files[base].append(fname)

# bases that have both a root and ≥1 commentary
bases = [b for b in root_files if b in comm_files]

# --------------------------------------------------------------------
# 3)  CREATE ONE NEGATIVE (_f) PER BASE  ------------------------------
# --------------------------------------------------------------------
for base in bases:
    neg_fname = f"{base}_f.txt"
    neg_path  = os.path.join(DATA_DIR, neg_fname)

    if os.path.exists(neg_path):
        print(f"⏩  Skipping {neg_fname} (already exists)")
        continue

    # pick a commentary from a DIFFERENT base
    other_base = random.choice([b for b in bases if b != base])
    src_comm   = random.choice(comm_files[other_base])
    src_path   = os.path.join(DATA_DIR, src_comm)

    shutil.copyfile(src_path, neg_path)
    print(f"✅  Created {neg_fname}   ←   {src_comm}")

print("Done ✔️")
