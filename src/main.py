from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import pandas as pd

from .reports import spend_by_category
from .views import index


def main() -> None:
    parser = argparse.ArgumentParser(description="Coursework 1 demo CLI")
    parser.add_argument("--datetime", default="2023-12-15 15:30:00", help="Datetime 'YYYY-MM-DD HH:MM:SS'")
    parser.add_argument("--file", default=str(Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"))
    args = parser.parse_args()

    print(index(args.datetime, args.file))

from .reports import spending_by_category
from .services import simple_search
from .utils import load_transactions
from .views import events, index

logging.basicConfig(level=logging.INFO)
if __name__ == "__main__":
    main()


def main() -> None:
    """Запустить демонстрацию."""
    data_path = Path(__file__).parents[1] / "data" / "operations.xlsx"
    df = load_transactions(data_path)
    txns = df.to_dict(orient="records")

    print("— index —")
    print(json.dumps(index("2025-04-23 12:00:00"), ensure_ascii=False, indent=2))
    print("\n— events —")
    print(json.dumps(events(df), ensure_ascii=False, indent=2))
    print("\n— simple_search —")
    print(json.dumps(simple_search("coffee", txns), ensure_ascii=False, indent=2))
    print("\n— spending_by_category —")
    print(
        json.dumps(
            spending_by_category(df, "Кафе", "2025-01-01"),
            ensure_ascii=False,
            indent=2,
        )
    )
    filepath = Path(__file__).parent.parent / "data" / "transactions.xlsx"
    if filepath.exists():
        df = pd.read_excel(filepath)
        print(spend_by_category(df, category="Супермаркеты"))
    else:
        print("Нет файла с транзакциями, пропускаем отчёт.")


if __name__ == "__main__":


