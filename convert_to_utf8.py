import os

FOLDER = "raw_tibetan_data"
POSSIBLE_ENCODINGS = ["utf-8", "utf-16-le", "utf-16-be", "utf-16", "cp1252", "latin-1"]

def convert_all_to_utf8(folder):
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)

        for enc in POSSIBLE_ENCODINGS:
            try:
                with open(path, "r", encoding=enc) as f:
                    content = f.read()
                # Save in UTF-8
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Converted {fname} from {enc} to UTF-8")
                break
            except UnicodeError:
                continue
        else:
            raise UnicodeError(f"❌ Could not decode {fname} using known encodings")

# ------------------ RUN ------------------
convert_all_to_utf8(FOLDER)