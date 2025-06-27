#!/usr/bin/env python3
import os, csv
from pathlib import Path
from collections import defaultdict

DATASETS = {
    "sanskrit_pairs.csv": "raw_sanskrit_data",
    "tibetan_pairs.csv":  "raw_tibetan_data",
}

def read_file(folder, fname):
    """Read and return the text of a file using strict UTF-8 decoding."""
    path = os.path.join(folder, fname)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().strip()



def make_csv(csv_name: str, folder: str):
    files = os.listdir(folder)

    # bucket every file by its base (stem without final suffix)
    by_base = defaultdict(list)
    for fname in files:
        stem = Path(fname).stem                      # no extension
        base, suffix = stem.rsplit("_", 1)           # e.g. ("bca_5.1", "root")
        by_base[base].append((suffix.lower(), fname))

    rows = []

    for base, items in by_base.items():
        root_file = f_file = pos_file = None

        for suf, fname in items:
            if suf == "root":
                root_file = fname
            elif suf == "f":
                f_file = fname
            else:                       # any commentary suffix (_p, _comm, _mua…)
                if pos_file is None:    # choose first one encountered
                    pos_file = fname

        # keep only complete triples
        if root_file and pos_file and f_file:
            root_text = read_file(folder, root_file)

            pos_text = read_file(folder, pos_file)
            rows.append([base, root_text, pos_text, True])

            neg_text = read_file(folder, f_file)
            rows.append([base, root_text, neg_text, False])

    # write CSV next to the script (change if you prefer inside folder)
    with open(csv_name, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["pair_id", "root", "commentary", "label"])
        for pair_id, root, comm, lbl in rows:
            writer.writerow([pair_id, root, comm, int(lbl)])  # 1/0 labels

    print(f"✅  {csv_name}: {len(rows)} rows written "
          f"({len(rows)//2} root texts)")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    for csv_file, data_dir in DATASETS.items():
        make_csv(csv_file, data_dir)
