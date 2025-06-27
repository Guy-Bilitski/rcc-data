import os, random, shutil
from collections import defaultdict

DATA_DIR = "raw_tibetan_data"
random.seed(42)

for entry in os.scandir(DATA_DIR):
    if entry.is_dir():
        subdir = entry.path
        for item in os.scandir(subdir):
            src = item.path
            dst = os.path.join(DATA_DIR, item.name)

            if os.path.exists(dst):
                name, ext = os.path.splitext(item.name)
                dst = os.path.join(DATA_DIR, f"{entry.name}_{name}{ext}")

            shutil.move(src, dst)

        # Only remove folder if truly empty
        if not os.listdir(subdir):
            try:
                os.rmdir(subdir)
            except PermissionError as e:
                print(f"❌ Cannot remove {subdir}: {e}")
        else:
            print(f"⚠️  Not empty, skipping deletion: {subdir}")

print("✔️  All files flattened into", DATA_DIR)
