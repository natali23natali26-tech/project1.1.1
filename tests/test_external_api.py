import pytest
from unittest.mock import patch, Mock
from src.external_api import get_exchange_rate

@pytest.fixture
def mock_env():
    with patch('os.getenv', return_value='mock_api_key'):
        yield

def test_get_exchange_rate_success(mock_env):
    with patch('requests.get') as mock_get:
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
        assert rate == 70.5

def test_get_exchange_rate_failure(mock_env):
    with patch('requests.get') as mock_get:
        # Настройка мока на ошибку при запросе
        mock_get.side_effect = Exception("Network Error")

        # Вызов функции и проверка результата
        rate = get_exchange_rate('USD')
        assert rate is None
