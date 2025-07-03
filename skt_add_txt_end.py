import os

folder = "raw_sanskrit_data"

for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, filename + ".txt")
        os.rename(old_path, new_path)

print("✅ Renaming complete.")
