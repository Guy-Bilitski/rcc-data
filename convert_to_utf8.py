import os
import chardet                     # optional but handy

FOLDER = "raw_tibetan_data"
POSSIBLE_ENCODINGS = [
    "utf-8",
    "utf-16",
    "utf-16-le",
    "utf-16-be",
    "mac_roman",      # ← NEW
    "cp1252",
    "latin-1",
]

def convert_file(path):
    for enc in POSSIBLE_ENCODINGS:
        try:
            with open(path, "r", encoding=enc) as fh:
                txt = fh.read()
            # quick sanity check: at least one ASCII letter
            if any("a" <= c <= "z" for c in txt.lower()):
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(txt)
                print(f"✅ {path}  ({enc} → utf-8)")
                return
        except UnicodeError:
            continue
    raise UnicodeError(f"❌ could not decode {path}")

def convert_tree(root):
    for rootdir, _dirs, files in os.walk(root):
        for f in files:
            convert_file(os.path.join(rootdir, f))

convert_tree(FOLDER)
