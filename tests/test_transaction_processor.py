import pytest
import re  # Необходим для тестов, работающих с регулярными выражениями
from unittest.mock import patch  # Импортируем patch из unittest.mock
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
    # Тест для функции поиска
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
    (['не существующий'], {}),
])
def test_process_bank_operations(categories, expected_result):
    # Тест для подсчета операций по категориям
    result = process_bank_operations(mock_data, categories)
    assert result == expected_result


@pytest.mark.parametrize("data, search", [
    ([
        {'description': 'Тестовая операция 1'},
        {'description': 'Тестовая операция 2'},
    ], 'тестовая'),
    ([
        {'description': 'Операция без совпадений'},
    ], 'xyz'),
])
def test_process_bank_search_with_mock(data, search):
    # Тест для функции поиска с использованием mock
    with patch('re.compile') as mock_compile:
        process_bank_search(data, search)
        mock_compile.assert_called_once_with(re.escape(search), re.IGNORECASE)


@pytest.mark.parametrize("data, categories", [
    ([
        {'description': 'Opera 1'},
        {'description': 'Opera 2'},
    ], ['opera']),
    ([{'description': 'No matches'}], ['xyz']),
])
def test_process_bank_operations_with_mock(data, categories):
    # Тест для функции подсчета операций с использованием mock
    with patch('collections.Counter') as mock_counter:
        process_bank_operations(data, categories)
        mock_counter.assert_called()
