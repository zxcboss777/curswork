"""
Вспомогательные функции, используемые во всех слоях приложения.
"""
"""Utility helpers for coursework project."""

from __future__ import annotations

import logging
import random
from datetime import datetime, time
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from .logger import logger

DATA_COL_DATE = "Дата операции"
DATA_COL_CARD = "Номер карты"
DATA_COL_PAYMENT = "Сумма платежа"
DATA_COL_CASHBACK = "Кешбэк"
DATA_COL_CATEGORY = "Категория"
DATA_COL_DESCRIPTION = "Описание"

def parse_datetime(value: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Преобразовать строку *value* в объект :class:`datetime.datetime`.
    Parameters
    ----------
    value:
        Строка вроде ``"2025-04-23 15:47:10"``.
    fmt:
        Формат строки (по умолчанию — `YYYY-MM-DD HH:MM:SS`).
    Raises
    ------
    ValueError
        При неверном формате даты.
    """
    try:
        return datetime.strptime(value, fmt)
    except ValueError as exc:  # pragma: no cover  # тестируем happy-path
        logger.error("parse_datetime: %s", exc, exc_info=exc)
        raise
GREETINGS = {
    "morning": "Доброе утро",
    "day": "Добрый день",
    "evening": "Добрый вечер",
    "night": "Доброй ночи",
}


def json_response(payload: Any) -> Dict[str, Any]:
    """
    Обернуть *payload* в стандартный JSON-ответ API.
def _get_part_of_day(now: time) -> str:
    if time(6, 0) <= now < time(12, 0):
        return GREETINGS["morning"]
    if time(12, 0) <= now < time(18, 0):
        return GREETINGS["day"]
    if time(18, 0) <= now < time(23, 0):
        return GREETINGS["evening"]
    return GREETINGS["night"]

    Возвращается словарь вида::

        {
            "result": <payload>,
            "generated_at": "2025-04-23T16:02:13.379352"
        }
    """
    return {"result": payload, "generated_at": datetime.now().isoformat()}
# ------------------------------------------------------------
# Public helpers
# ------------------------------------------------------------


def send_greeting(date_time: datetime | None = None) -> str:
    """Return greeting phrase depending on *date_time*."""
    date_time = date_time or datetime.now()
    greeting = _get_part_of_day(date_time.time())
    logger.debug("Greeting generated: %s", greeting)
    return greeting


def read_transactions(xlsx_path: str | Path) -> pd.DataFrame:
    """Read Excel file with bank transactions into *pandas* DataFrame."""
    df = pd.read_excel(xlsx_path)
    logger.info("Loaded %s transactions from %s", len(df), xlsx_path)
    return df


def card_info(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Aggregate total spent & cashback for every card."""
    summaries = []
    for last_digits, group in df.groupby(DATA_COL_CARD):
        total = float(group[DATA_COL_PAYMENT].sum())
        cashback = float(group[DATA_COL_CASHBACK].sum())
        summaries.append(
            {
                "last_digits": str(last_digits),
                "total_spent": round(total, 2),
                "cashback": round(cashback, 2),
            }
        )
    logger.debug("Card info calculated: %s", summaries)
    return summaries


def top_transactions(df: pd.DataFrame, limit: int = 5) -> List[Dict[str, Any]]:
    df_sorted = df.reindex(df[DATA_COL_PAYMENT].abs().sort_values(ascending=False).index).head(limit)
    res = df_sorted[[DATA_COL_DATE, DATA_COL_PAYMENT, DATA_COL_CATEGORY, DATA_COL_DESCRIPTION]].to_dict(
        orient="records"
    )
    logger.debug("Top %d transactions: %s", limit, res)
    return res

def load_transactions(xls_path: str | Path) -> pd.DataFrame:

# ---------------- External data (stubs) ----------------------


def _dummy_price() -> float:
    return round(random.uniform(50, 500), 2)


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Return list of dicts with fake currency rates.
    Replace with real API call if needed.
    """
    Загрузить Excel-файл *operations.xlsx* и вернуть :class:`pandas.DataFrame`.
    rates = [{"currency": cur, "rate": _dummy_price()} for cur in currencies]
    logger.info("Stub currency rates generated for %s", currencies)
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Return list of dicts with fake stock prices.
    Такой &laquo;тонкий&raquo; слой позволяет позже поменять источник данных
    (например, на PostgreSQL или REST-API) без изменения бизнес-логики.
    Replace with real API call if needed.
    """
    path = Path(xls_path)
    if not path.exists():  # pragma: no cover
        raise FileNotFoundError(f"{path} not found")
    return pd.read_excel(path)
    prices = [{"stock": st, "price": _dummy_price()} for st in stocks]
    logger.info("Stub stock prices generated for %s", stocks)
    return prices


def format_money(amount: float, currency: str = "USD") -> str:
    return f"{amount:,.2f} {currency}"

