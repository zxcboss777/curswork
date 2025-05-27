"""
Функции-контроллеры *страниц*:
— &laquo;Главная&raquo; (`index`)
— &laquo;События&raquo; (`events`)
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import pandas as pd

# собственный логгер проекта
from .logger import logger
# бизнес-утилиты
from .utils import (card_info, get_currency_rates, get_stock_prices,
                    json_response, read_transactions, send_greeting,
                    top_transactions)

# ──────────────────────────────────────────────────────────────────────────

USER_SETTINGS_FILE = (
    Path(__file__).resolve().parent.parent / "user_settings.json"
)
DEFAULT_SETTINGS = {
    "user_currencies": ["USD", "EUR"],
    "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
}


def _load_settings() -> Dict[str, Any]:
    """
    Читает `user_settings.json`; если файла нет — возвращает `DEFAULT_SETTINGS`.
    """
    if USER_SETTINGS_FILE.exists():
        text = USER_SETTINGS_FILE.read_text(encoding="utf-8")
        return json.loads(text)
    return DEFAULT_SETTINGS


# ──────────────────────────────────────────────────────────────────────────
# views
# ──────────────────────────────────────────────────────────────────────────
def index(date_time_str: str, xlsx_path: str | Path | None = None) -> str:
    """
    &laquo;Главная&raquo; страница.

    Parameters
    ----------
    date_time_str
        Дата/время от клиента (&laquo;YYYY-MM-DD HH:MM:SS&raquo;).
    xlsx_path
        Альтернативный путь к *operations.xlsx* (опционально).

    Returns
    -------
    str
        Красиво отформатированный JSON-текст, удовлетворяющий ТЗ.
    """
    dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    settings = _load_settings()

    data_file = (
        Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"
    )
    df = read_transactions(xlsx_path or data_file)

    response: Dict[str, Any] = {
        "greeting": send_greeting(dt),
        "cards": card_info(df),
        "top_transactions": top_transactions(df),
        "currency_rates": get_currency_rates(
            settings["user_currencies"]
        ),
        "stock_prices": get_stock_prices(
            settings["user_stocks"]
        ),
    }

    logger.info("Index page JSON generated.")
    return json.dumps(response, ensure_ascii=False, indent=2)


def events(df: pd.DataFrame) -> Dict[str, Any]:
    """
    &laquo;События&raquo; — минимальная выборка из *df* (первые 5 записей).

    Parameters
    ----------
    df
        Таблица транзакций.

    Returns
    -------
    dict
        JSON с полем ``events``.
    """
    selection = (
        df.head()
        .assign(date=lambda d: d["date"].dt.strftime("%Y-%m-%d"))
        .to_dict(orient="records")
    )
    return json_response({"events": selection})



