import pytest
from unittest.mock import patch, mock_open

import os
import json
from src.utils import load_transactions, convert_to_rub  # Импортируем из src


@pytest.fixture
def mock_path_exists():
    with patch('os.path.exists') as mock_exists:
        yield mock_exists


def test_load_transactions_success(mock_path_exists):
    """Тестирование успешной загрузки транзакций из файла."""
    mock_path_exists.return_value = True
    with patch("builtins.open", mock_open(read_data='[{"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}]')) as mock_file:
        transactions = load_transactions('dummy_path.json')
        assert len(transactions) == 1
        assert transactions[0]['operationAmount']['amount'] == 100
        assert transactions[0]['operationAmount']['currency']['code'] == 'USD'


def test_load_transactions_file_not_found(mock_path_exists):
    """Тестирование отсутствия файла."""
    mock_path_exists.return_value = False
    transactions = load_transactions('dummy_path.json')
    assert transactions == []


def test_load_transactions_invalid_json(mock_path_exists):
    """Тестирование обработки некорректного JSON."""
    mock_path_exists.return_value = True
    with patch("builtins.open", mock_open(read_data='invalid json')) as mock_file:
        transactions = load_transactions('dummy_path.json')
        assert transactions == []


@pytest.fixture
def mock_get_exchange_rate():
    with patch('src.utils.get_mock_exchange_rate') as mock:
        yield mock


def test_convert_to_rub_usd(mock_get_exchange_rate):
    """Тестирование конвертации из USD в RUB."""
    mock_get_exchange_rate.return_value = 90.0
    transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}
    result = convert_to_rub(transaction)
    assert result == 9000.0


def test_convert_to_rub_rub():
    """Тестирование, когда валюта уже в RUB."""
    transaction = {"operationAmount": {"amount": 100, "currency": {"code": "RUB"}}}
    result = convert_to_rub(transaction)
    assert result == 100.0


def test_convert_to_rub_no_rate(mock_get_exchange_rate):
    """Тестирование, когда курс валюты не найден."""
    mock_get_exchange_rate.return_value = None
    transaction = {"operationAmount": {"amount": 100, "currency": {"code": "GBP"}}}
    result = convert_to_rub(transaction)
    assert result == 0.0


def test_convert_to_rub_missing_data():
    """Тестирование, когда отсутствуют данные в транзакции."""
    transaction = {}
    result = convert_to_rub(transaction)
    assert result == 0.0


def test_convert_to_rub_invalid_amount():
    """Тестирование, когда сумма имеет некорректный тип."""
    transaction = {"operationAmount": {"amount": "abc", "currency": {"code": "USD"}}}
    with pytest.raises(ValueError):
        convert_to_rub(transaction)
