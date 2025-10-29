import pytest
from src.transaction_processor import process_bank_search, process_bank_operations

# Тестовые данные
mock_data = [
    {'description': 'Перевод организации', 'amount': 100, 'currency_code': 'RUB'},
    {'description': 'Перевод с карты на карту', 'amount': 200, 'currency_code': 'USD'},
    {'description': 'Платеж за услуги', 'amount': 150, 'currency_code': 'EUR'},
    {'description': 'Вывод наличных', 'amount': 50, 'currency_code': 'RUB'},
]


@pytest.mark.parametrize("search_term, expected_result", [
    ('перевод', [
        {'description': 'Перевод организации', 'amount': 100, 'currency_code': 'RUB'},
        {'description': 'Перевод с карты на карту', 'amount': 200, 'currency_code': 'USD'},
    ]),
    ('платеж', [
        {'description': 'Платеж за услуги', 'amount': 150, 'currency_code': 'EUR'},
    ]),
    ('вывод', [
        {'description': 'Вывод наличных', 'amount': 50, 'currency_code': 'RUB'},
    ]),
    ('не существующий запрос', []),
])
def test_process_bank_search(search_term, expected_result):
    result = process_bank_search(mock_data, search_term)
    assert result == expected_result


@pytest.mark.parametrize("categories, expected_result", [
    (['перевод', 'платеж'], {
        'перевод': 2,
        'платеж': 1,
    }),
    (['вывод'], {
        'вывод': 1,
    }),
])
def test_process_bank_operations(categories, expected_result):
    result = process_bank_operations(mock_data, categories)
    assert result == expected_result
