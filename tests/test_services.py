from unittest.mock import patch

from src.services import investment_bank

TRANSACTIONS = [
    {"Дата операции": "2023-12-05", "Сумма операции": 101.0},
    {"Дата операции": "2023-12-10", "Сумма операции": 249.0},
]


@patch("src.services.requests.get")
def test_get_rates(mock_get):
    mock_get.return_value.json.return_value = {"data": {"EUR": {"value": 0.9}}}
    mock_get.return_value.raise_for_status = lambda: None


def test_investment_bank():
    saved = investment_bank("2023-12", TRANSACTIONS, 50)
    assert abs(saved - ((150 - 101) + (250 - 249))) < 1e-6

    # <‑‑‑ ключевой момент: подменяем константу внутри модуля
    with patch("src.services.API_KEY", "dummy_key"):
        from src.services import get_rates

        assert get_rates("USD")["EUR"] == 0.9



