#!/usr/bin/env python3
import os, unicodedata, re
from pathlib import Path

DATA_DIR = "raw_tibetan_data"

# --- helper: decide if a file looks like the mojibake you posted --------
CJK   = re.compile(r"[\u4E00-\u9FFF]")        # Chinese/Japanese/Korean
PUA   = re.compile(r"[\uE000-\uF8FF]")        # Private-Use Area
BOXES = re.compile(r"\uFFFD")                 # replacement “�”

def looks_like_the_mojibake(text:str) -> bool:
    """
    True  → file is almost certainly corrupted (CJK / PUA dominates, no ascii‐Wylie, no Tibetan)
    False → file is probably OK (Wylie transliteration or real Tibetan Unicode)
    """
    n = len(text)
    if n == 0:
        return False

    cjk   = len(CJK.findall(text))
    pua   = len(PUA.findall(text))
    boxes = len(BOXES.findall(text))

    # ratio of “weird” code-points
    ratio = (cjk + pua + boxes) / n

    # If >30 % of the characters are CJK / PUA / replacement, call it junk.
    return ratio > 0.30


# --- scan ----------------------------------------------------------------
bad = []
for p in Path(DATA_DIR).iterdir():
    if p.is_file():
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
            if looks_like_the_mojibake(txt):
                bad.append(p.name)
        except Exception as e:
            # even UTF-8 reading failed → definitely bad
            bad.append(p.name)
            print(f"❌ {p.name} could not even be read ({e})")

# --- report --------------------------------------------------------------
if bad:
    print("\n📄 Suspected corrupted files:")
    for name in bad:
        print("   •", name)
else:
    print("✅ No corrupted files detected.")
