from unittest.mock import patch

import pytest

from src.services import simple_search


@patch("src.services.requests.get")
def test_get_rates(mock_get):
    mock_get.return_value.json.return_value = {"data": {"EUR": {"value": 0.9}}}
    mock_get.return_value.raise_for_status = lambda: None

@pytest.fixture
def txns():
    return [
        {"description": "Coffee shop", "amount": -300},
        {"description": "Grocery store", "amount": -1500},
    ]
    # <‑‑‑ ключевой момент: подменяем константу внутри модуля
    with patch("src.services.API_KEY", "dummy_key"):
        from src.services import get_rates


def test_simple_search_found(txns):
    result = simple_search("coffee", txns)
    assert result["count"] == 1
    assert result["items"][0]["description"] == "Coffee shop"


def test_simple_search_not_found(txns):
    assert simple_search("cinema", txns)["count"] == 0
        assert get_rates("USD")["EUR"] == 0.9
