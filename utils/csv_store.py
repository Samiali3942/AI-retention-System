import os
import pandas as pd


def ensure_directory(path: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def read_csv_safe(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def write_csv_safe(df: pd.DataFrame, path: str, index: bool = False) -> None:
    ensure_directory(path)
    df.to_csv(path, index=index)


def append_csv(df: pd.DataFrame, path: str, index: bool = False) -> None:
    ensure_directory(path)
    if os.path.exists(path):
        existing = pd.read_csv(path)
        combined = pd.concat([existing, df], ignore_index=True)
        combined.to_csv(path, index=index)
    else:
        df.to_csv(path, index=index)


