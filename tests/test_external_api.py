import unittest
from unittest.mock import patch, Mock
from src.external_api import get_exchange_rate


class TestGetExchangeRate(unittest.TestCase):

    @patch('requests.get')
    @patch('os.getenv')
    def test_get_exchange_rate_success(self, mock_getenv, mock_get):
        # Настройка переменной окружения
        mock_getenv.return_value = 'mock_api_key'

        # Настройка мока для ответа от requests.get
        mock_response = Mock()
        mock_response.json.return_value = {
            'rates': {
                'USD': 70.5
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Вызов функции и проверка результата
        rate = get_exchange_rate('USD')
        self.assertEqual(rate, 70.5)

    @patch('requests.get')
    @patch('os.getenv')
    def test_get_exchange_rate_failure(self, mock_getenv, mock_get):
        # Настройка переменной окружения
        mock_getenv.return_value = 'mock_api_key'

        # Настройка мока на ошибку при запросе
        mock_get.side_effect = Exception("Network Error")

        # Вызов функции и проверка результата
        rate = get_exchange_rate('USD')
        self.assertIsNone(rate)


if __name__ == '__main__':
    unittest.main()
