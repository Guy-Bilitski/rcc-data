from pathlib import Path

# Define the tibetan folder
folder = Path("raw_tibetan_data")

# Iterate over all files recursively
for file in folder.rglob("*"):
    if file.is_file() and file.stem.endswith("_f"):
        print(f"Deleting: {file}")
        file.unlink()
