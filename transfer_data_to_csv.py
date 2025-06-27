#!/usr/bin/env python3
import os, csv, re
from pathlib import Path
from collections import defaultdict

DATASETS = {
    "sanskrit_pairs.csv": "raw_sanskrit_data",
    "tibetan_pairs.csv":  "raw_tibetan_data",
}

SUFFIX_RX = re.compile(r"(.*?)(?:_)?([A-Za-z]+)$")  # capture base + suffix

def read_file(folder: str, fname: str) -> str:
    with open(Path(folder) / fname, "r", encoding="utf-8") as fh:
        return fh.read().strip()

def make_csv(csv_name: str, folder: str):
    by_base = defaultdict(list)           # base → [(suffix, filename), …]

    for fname in os.listdir(folder):
        stem = Path(fname).stem           # drop extension

        m = SUFFIX_RX.fullmatch(stem)
        if not m:
            print(f"⚠️  Skipping {fname} (no suffix found)")
            continue

        base, suffix = m.group(1), m.group(2).lower()
        by_base[base].append((suffix, fname))

    rows = []

    for base, items in by_base.items():
        root_file = f_file = pos_file = None

        for suf, fname in items:
            if suf == "root":
                root_file = fname
            elif suf == "f":
                f_file = fname
            else:                         # any other suffix = positive comm
                pos_file = pos_file or fname

        if root_file and pos_file and f_file:
            root_txt = read_file(folder, root_file)
            rows.append([base, root_txt,
                         read_file(folder, pos_file), 1])
            rows.append([base, root_txt,
                         read_file(folder, f_file),   0])

    # write CSV
    with open(csv_name, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["pair_id", "root", "commentary", "label"])
        writer.writerows(rows)

    print(f"✅ {csv_name}: {len(rows)} rows "
          f"({len(rows)//2} root texts)")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    for csv_file, data_dir in DATASETS.items():
        make_csv(csv_file, data_dir)
