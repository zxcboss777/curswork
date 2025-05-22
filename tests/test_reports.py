import pandas as pd

from src.reports import spend_by_category, spending_by_category


def test_spending_by_category(sample_df):
    report = spending_by_category(sample_df, "Кафе", "2025-01-01")
    assert report["total_spent"] == -950  # -300-450-200
    assert len(report["daily_breakdown"]) == 3
df = pd.DataFrame(
    {
        "Дата операции": ["2023-10-10", "2023-11-05", "2023-12-01"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Кафе и рестораны"],
        "Сумма платежа": [100, 150, 200],
    }
)


def test_spend_by_category(tmp_path):
    res = spend_by_category(df, "Супермаркеты", "2023-12-15")
    assert res["total_spent"] == 250
