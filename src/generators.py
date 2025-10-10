from typing import Generator, Dict, Any


def filter_by_currency(transactions: Generator[Dict[str, Any], None, None], currency_code: str) -> Generator[Dict[str, Any], None, None]:
    """Фильтрует транзакции по заданной валюте и возвращает итератор."""
    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == currency_code:
            yield transaction


def transaction_descriptions(
        transactions: Generator[Dict[str, Any], None, None]
) -> Generator[str, None, None]:
    """Генерирует описания транзакций."""
    for transaction in transactions:
        yield transaction['description']


def card_number_generator(start: int,
                          stop: int) -> Generator[str, None, None]:
    """Генерирует номера банковских карт
    в заданном диапазоне."""
    for num in range(start, stop + 1):
        yield (f"{num:016d}"[:4] + " " + f"{num:016d}"[4:8] + " " +
               f"{num:016d}"[8:12] + " " + f"{num:016d}"[12:16])
