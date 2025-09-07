import pytest
from processing import filter_by_state, sort_by_date

# Тестирование функции filter_by_state
@pytest.mark.parametrize(
    "input_data, state, expected_output",
    [
        (
            [
                {'id': 1, 'state': 'EXECUTED'},
                {'id': 2, 'state': 'CANCELED'},
                {'id': 3, 'state': 'EXECUTED'}
            ],
            'EXECUTED',
            [
                {'id': 1, 'state': 'EXECUTED'},
                {'id': 3, 'state': 'EXECUTED'}
            ]
        ),
        (
            [
                {'id': 1, 'state': 'CANCELED'},
                {'id': 2, 'state': 'CANCELED'},
            ],
            'EXECUTED',
            []  # Отсутствие словарей с указанным статусом
        ),
        (
            [
                {'id': 1, 'state': 'EXECUTED'},
                {'id': 2, 'state': 'PENDING'},
                {'id': 3, 'state': 'EXECUTED'}
            ],
            'CANCELED',
            []  # Отсутствие словарей с указанным статусом
        ),
    ]
)
def test_filter_by_state(input_data, state, expected_output):
    """
    Тестирует функцию filter_by_state с разными параметрами.
    """
    assert filter_by_state(input_data, state) == expected_output


# Тестирование функции sort_by_date
@pytest.mark.parametrize(
    "input_data, reverse, expected_output",
    [
        (
            [
                {'id': 1, 'date': '2022-04-01T15:00:00'},
                {'id': 2, 'date': '2022-01-01T15:00:00'},
                {'id': 3, 'date': '2022-03-01T15:00:00'}
            ],
            True,
            [
                {'id': 1, 'date': '2022-04-01T15:00:00'},
                {'id': 3, 'date': '2022-03-01T15:00:00'},
                {'id': 2, 'date': '2022-01-01T15:00:00'}
            ]
        ),
        (
            [
                {'id': 1, 'date': '2022-01-01T15:00:00'},
                {'id': 2, 'date': '2022-01-01T15:00:00'},
                {'id': 3, 'date': '2022-02-01T15:00:00'}
            ],
            False,
            [
                {'id': 1, 'date': '2022-01-01T15:00:00'},
                {'id': 2, 'date': '2022-01-01T15:00:00'},
                {'id': 3, 'date': '2022-02-01T15:00:00'}
            ]
        ),
        (
            [
                {'id': 1, 'date': 'invalid_date'},
                {'id': 2, 'date': '2022-01-01T15:00:00'}
            ],
            True,
            [
                {'id': 2, 'date': '2022-01-01T15:00:00'},
                {'id': 1, 'date': 'invalid_date'}  # Неверный формат даты должен идти в конце
            ]
        )
    ]
)
def test_sort_by_date(input_data, reverse, expected_output):
    """
    Тестирует функцию sort_by_date на различных входных данных.
    """
    assert sort_by_date(input_data, reverse) == expected_output

# Проверка корректности на некорректных датах
@pytest.mark.parametrize(
    "input_data, reverse",
    [
        (
            [
                {'id': 1, 'date': '2022-01-01T15:00:00'},
                {'id': 2, 'date': 'not_a_date'}
            ],
            True
        ),
        (
            [
                {'id': 1, 'date': 'invalid_date'},
                {'id': 2, 'date': None}
            ],
            False
        )
    ]
)
def test_sort_by_date_invalid_formats(input_data, reverse):
    """
    Тестирует функцию sort_by_date на некорректные форматы дат.
    """
    with pytest.raises(ValueError):
        sort_by_date(input_data, reverse)
