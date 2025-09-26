import unittest
from unittest.mock import patch, mock_open
import sys
import os

from src.utils import load_transactions, convert_to_rub  # Импортируем из src

# Добавляем корневой путь проекта в sys.path для импортирования модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class TestLoadTransactions(unittest.TestCase):

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"amount": 100, "currency": "USD"}]')
    def test_load_transactions_success(self, mock_file, mock_exists):
        """Тестирование успешной загрузки транзакций из файла."""
        mock_exists.return_value = True
        transactions = load_transactions('dummy_path.json')
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['amount'], 100)
        self.assertEqual(transactions[0]['currency'], 'USD')

    @patch('os.path.exists')
    def test_load_transactions_file_not_found(self, mock_exists):
        """Тестирование отсутствия файла."""
        mock_exists.return_value = False
        transactions = load_transactions('dummy_path.json')
        self.assertEqual(transactions, [])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_transactions_invalid_json(self, mock_file, mock_exists):
        """Тестирование обработки некорректного JSON."""
        mock_exists.return_value = True
        mock_file.side_effect = [mock_open(read_data='invalid json').return_value]
        transactions = load_transactions('dummy_path.json')
        self.assertEqual(transactions, [])
