import pytest

# Импортируем функции, которые будем тестировать
from src.generators import (card_number_generator,
                            filter_by_currency,
                            transaction_descriptions)


# Тесты для функции filter_by_currency
@pytest.mark.parametrize("transactions, currency_code, expected", [
    ([
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"operationAmount": {"currency": {"code": "USD"}}}
    ], "USD", 2),  # Две транзакции USD
    ([
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}}
    ], "USD", 0),  # Нет транзакций USD
    ([], "USD", 0),  # Пустой список
])
def test_filter_by_currency(transactions, currency_code, expected):
    filtered_transactions = list(
        filter_by_currency(transactions, currency_code))
    assert len(filtered_transactions) == expected


# Тесты для функции transaction_descriptions
@pytest.mark.parametrize("transactions, expected_descriptions", [
    ([
        {"description": "перевод 1"},
        {"description": "перевод 2"},
    ], ["перевод 1", "перевод 2"]),  # Ожидаем 2 описания
    ([
        {"description": "перевод 1"},
    ], ["перевод 1"]),  # Ожидаем 1 описание
    ([], []),  # Пустой список, ожидаем пустой результат
])
def test_transaction_descriptions(transactions, expected_descriptions):
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == expected_descriptions


# Тесты для card_number_generator
@pytest.mark.parametrize("start, stop, expected_numbers", [
    (1, 5, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]),
    (0, 0, ["0000 0000 0000 0000"]),  # Ожидаем только 1 номер
    (999, 1002, [
        "0000 0000 0000 0999",
        "0000 0000 0000 1000",
        "0000 0000 0000 1001",
        "0000 0000 0000 1002",
    ]),  # Проверяем, что границы работают правильно
])
def test_card_number_generator(start, stop, expected_numbers):
    generated_numbers = list(card_number_generator(start, stop))
    assert generated_numbers == expected_numbers
