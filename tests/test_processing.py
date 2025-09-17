import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстуры для удобства использования данных в тестах
@pytest.fixture
def executed_transaction():
    return {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01T10:00:00'}


@pytest.fixture
def canceled_transaction():
    return {'id': 2, 'state': 'CANCELED', 'date': '2023-01-02T10:00:00'}


@pytest.fixture
def pending_transaction():
    return {'id': 3, 'state': 'PENDING', 'date': '2023-01-03T10:00:00'}


# Тестирование функции filter_by_state
@pytest.mark.parametrize(
    "input_data, state, expected_output",
    [
        ([{'id': 1, 'state': 'EXECUTED'},
          {'id': 2, 'state': 'CANCELED'},
          {'id': 3, 'state': 'EXECUTED'}],
         'EXECUTED', [{'id': 1, 'state': 'EXECUTED'},
                      {'id': 3, 'state': 'EXECUTED'}]),
        ([{'id': 1, 'state': 'CANCELED'},
          {'id': 2, 'state': 'CANCELED'}],
         'EXECUTED', []),
        ([{'id': 1, 'state': 'EXECUTED'},
          {'id': 2, 'state': 'PENDING'},
          {'id': 3, 'state': 'EXECUTED'}],
         'CANCELED', []),
    ]
)
def test_filter_by_state(input_data, state, expected_output):
    assert filter_by_state(input_data, state) == expected_output


# Тестирование функции sort_by_date (только для корректных дат)
@pytest.mark.parametrize(
    "input_data, reverse, expected_output",
    [
        (
            [{'id': 1, 'date': '2022-04-01T15:00:00'},
             {'id': 2, 'date': '2022-01-01T15:00:00'},
             {'id': 3, 'date': '2022-03-01T15:00:00'}],
            True,
            [{'id': 1, 'date': '2022-04-01T15:00:00'},
             {'id': 3, 'date': '2022-03-01T15:00:00'},
             {'id': 2, 'date': '2022-01-01T15:00:00'}]
        ),
        (
            [{'id': 1, 'date': '2022-01-01T15:00:00'},
             {'id': 2, 'date': '2022-01-01T15:00:00'},
             {'id': 3, 'date': '2022-02-01T15:00:00'}],
            False,
            [{'id': 1, 'date': '2022-01-01T15:00:00'},
             {'id': 2, 'date': '2022-01-01T15:00:00'},
             {'id': 3, 'date': '2022-02-01T15:00:00'}]
        ),
    ]
)
def test_sort_by_date(input_data, reverse, expected_output):
    """Тест сортировки по дате для корректных форматов."""
    assert sort_by_date(input_data, reverse) == expected_output


# Тестирование функции sort_by_date с некорректными датами (ожидаем исключение)
@pytest.mark.parametrize(
    "input_data, reverse",
    [
        ([{'id': 1, 'date': '2022-01-01T15:00:00'},
          {'id': 2, 'date': 'not_a_date'}], True),
        ([{'id': 1, 'date': 'invalid_date'},
          {'id': 2, 'date': None}], False)
    ]
)
def test_sort_by_date_invalid_formats(input_data, reverse):
    """Тест на выброс исключения ValueError при некорректном формате даты."""
    with pytest.raises(ValueError):
        sort_by_date(input_data, reverse)
