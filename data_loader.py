from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "dataset_practic.csv"

FEATURE_COLUMNS = [
    "alcohol",
    "malic_acid",
    "ash",
    "alcalinity_of_ash",
    "magnesium",
    "total_phenols",
    "flavanoids",
    "nonflavanoid_phenols",
    "proanthocyanins",
    "color_intensity",
    "hue",
    "phenolic_index",
    "proline",
]

DATASET_COLUMNS = ["target"] + FEATURE_COLUMNS


class DatasetLoadError(RuntimeError):
    pass


def load_wine_dataset():
    """
    Датасет лежит локально в папке data.
    Внешней загрузки нет: данные читаются из локального файла.
    """
    if not DATASET_PATH.exists():
        raise DatasetLoadError(f"Файл датасета не найден: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH, header=None, names=DATASET_COLUMNS)

    if df.shape[1] != len(DATASET_COLUMNS):
        raise DatasetLoadError("В датасете должно быть 14 колонок: target + 13 признаков.")

    df = df.apply(pd.to_numeric, errors="coerce")
    if df.isnull().any().any():
        raise DatasetLoadError("В датасете найдены некорректные или пустые значения.")

    label_encoder = LabelEncoder()
    df["target"] = label_encoder.fit_transform(df["target"])

    X = df[FEATURE_COLUMNS]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    return X_train, X_test, y_train, y_test, df
