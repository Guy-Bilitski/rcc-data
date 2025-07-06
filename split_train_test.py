# split_pairs.py
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

LABEL_COL = "label"

def split_file(csv_path: Path, test_size: int = 400, seed: int = 42):
    df = pd.read_csv(csv_path)
    assert df[LABEL_COL].isin([0, 1]).all(), f"{csv_path}: non-binary labels found"
    assert len(df) > test_size,         f"{csv_path}: not enough rows for {test_size}-row test set"

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        stratify=df[LABEL_COL],
        random_state=seed,
    )
    train_df.to_csv(csv_path.with_stem(csv_path.stem + "_train"), index=False)
    test_df.to_csv(csv_path.with_stem(csv_path.stem + "_test"),   index=False)
    print(f"✓ {csv_path.name}: {len(train_df)} train / {len(test_df)} test (stratified)")

for name in ["sanskrit_pairs.csv", "tibetan_pairs.csv"]:
    split_file(Path(name))
