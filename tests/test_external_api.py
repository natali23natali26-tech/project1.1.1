import pytest
from unittest.mock import patch


from src.external_api import get_exchange_rate

@pytest.fixture
def mock_env():
    with patch('os.getenv', return_value='mock_api_key'):
        yield


@patch('requests.get')
def test_get_exchange_rate_success(mock_get):
    mock_get.return_value.json.return_value = {'rates': {'RUB': 70.5 }}
    mock_get.return_value.status_code = 200
    rate = get_exchange_rate('USD')
    assert rate == 70.5


def test_get_exchange_rate_failure(mock_env):
    with patch('requests.get') as mock_get:
        # Настройка мока на ошибку при запросе
        mock_get.side_effect = Exception("Network Error")

        # Вызов функции и проверка результата
        rate = get_exchange_rate('USD')
        assert rate is None
