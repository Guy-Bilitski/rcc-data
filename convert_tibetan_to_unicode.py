# convert_tibetan_to_unicode.py
from pathlib import Path
import pyewts

SRC_DIR  = Path("raw_tibetan_data")    # where your EWTS .txt files live
OUT_DIR  = Path("unicode_output")      # results go here (will be created)
OUT_DIR.mkdir(exist_ok=True)

conv = pyewts.pyewts()                 # one converter is enough

for f in SRC_DIR.glob("*.txt"):
    out_lines = []
    with f.open(encoding="utf-8") as fin:
        for ln_no, line in enumerate(fin, 1):
            stripped = line.rstrip("\n")
            if not stripped:                 # keep blank lines as-is
                out_lines.append("")
                continue
            try:
                uni = conv.toUnicode(stripped)
            except Exception as e:
                # ➊ log the problem, ➋ fall back to the original text
                print(f"⚠️  {f.name}:{ln_no}: {e} – keeping EWTS unchanged")
                uni = stripped
            out_lines.append(uni)
    (OUT_DIR / f.name).write_text("\n".join(out_lines), encoding="utf-8")
    print(f"✅ {f.name} → {OUT_DIR/f.name}")
