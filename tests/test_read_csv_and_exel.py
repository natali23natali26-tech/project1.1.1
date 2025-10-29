from unittest.mock import patch
import pandas as pd
from src.read_csv_and_exel import read_transactions_from_csv, read_transactions_from_excel


def test_read_transactions_from_csv_success():
    # Тест проверки успешного чтения транзакций из CSV файла
    with patch("pandas.read_csv") as mock_read_csv:  # Используем мок для функции read_csv
        # Создаем тестовый DataFrame
        mock_df = pd.DataFrame({'id': [650703, 3598919],
                                'state': ['EXECUTED', 'EXECUTED'],
                                'date': ['2023-09-05T11:30:32Z', '2020-12-06T23:00:58Z'],
                                'amount': [16210, 29740],
                                'currency_name': ['Sol', 'Peso'],
                                'currency_code': ['PEN', 'COP'],
                                'from': ['Счет 58803664561298323391', 'Discover 3172601889670065'],
                                'to': ['Счет 39745660563456619397', 'Discover 0720428384694643'],
                                'description': ['Перевод организации', 'Перевод с карты на карту']})
        mock_read_csv.return_value = mock_df  # Настраиваем возвращаемое значение для мока

        # Вызываем функцию, которую тестируем
        result = read_transactions_from_csv('dummy_path.csv')

        # Проверяем, что результат соответствует ожидаемому
        expected_result = [
            {'id': 650703, 'state': 'EXECUTED', 'date': '2023-09-05T11:30:32Z', 'amount': 16210,
             'currency_name': 'Sol', 'currency_code': 'PEN',
             'from': 'Счет 58803664561298323391', 'to': 'Счет 39745660563456619397',
             'description': 'Перевод организации'},
            {'id': 3598919, 'state': 'EXECUTED', 'date': '2020-12-06T23:00:58Z', 'amount': 29740,
             'currency_name': 'Peso', 'currency_code': 'COP',
             'from': 'Discover 3172601889670065', 'to': 'Discover 0720428384694643',
             'description': 'Перевод с карты на карту'}
        ]
        assert result == expected_result

        # Проверяем, что read_csv была вызвана с правильным аргументом и параметрами
        mock_read_csv.assert_called_once_with('dummy_path.csv', sep=';', header=0)


def test_read_transactions_from_csv_file_not_found(capsys):
    # Тест проверки обработки ошибки при отсутствии файла CSV
    with patch("pandas.read_csv", side_effect=FileNotFoundError):
        result = read_transactions_from_csv('non_existent_file.csv')  # Вызываем функцию

        assert result == []  # Проверяем, что результат пустой
        captured = capsys.readouterr()  # Считываем вывод в stdout
        # Проверяем, что вывод содержит правильное сообщение об ошибке
        assert "Ошибка: Файл не найден по пути non_existent_file.csv" in captured.out


def test_read_transactions_from_csv_general_exception(capsys):
    # Тест проверки обработки общей ошибки при чтении CSV файла
    with patch("pandas.read_csv", side_effect=Exception("Some error")):
        result = read_transactions_from_csv('dummy_path.csv')  # Вызываем функцию

        assert result == []  # Проверяем, что результат пустой
        captured = capsys.readouterr()  # Считываем вывод в stdout
        # Проверяем, что вывод содержит правильное сообщение об ошибке
        assert "Ошибка при чтении CSV-файла: Some error" in captured.out


def test_read_transactions_from_excel_success():
    # Тест проверки успешного чтения транзакций из Excel файла
    with patch("pandas.read_excel") as mock_read_excel:  # Используем мок для функции read_excel
        # Создаем тестовый DataFrame
        mock_df = pd.DataFrame({'id': [650703, 3598919],
                                'state': ['EXECUTED', 'EXECUTED'],
                                'date': ['2023-09-05T11:30:32Z', '2020-12-06T23:00:58Z'],
                                'amount': [16210, 29740],
                                'currency_name': ['Sol', 'Peso'],
                                'currency_code': ['PEN', 'COP'],
                                'from': ['Счет 58803664561298323391', 'Discover 3172601889670065'],
                                'to': ['Счет 39745660563456619397', 'Discover 0720428384694643'],
                                'description': ['Перевод организации', 'Перевод с карты на карту']})
        mock_read_excel.return_value = mock_df  # Настраиваем возвращаемое значение для мока

        # Вызываем функцию, которую тестируем
        result = read_transactions_from_excel('dummy_path.xlsx')

        # Проверяем, что результат соответствует ожидаемому
        expected_result = [
            {'id': 650703, 'state': 'EXECUTED', 'date': '2023-09-05T11:30:32Z', 'amount': 16210,
             'currency_name': 'Sol', 'currency_code': 'PEN',
             'from': 'Счет 58803664561298323391', 'to': 'Счет 39745660563456619397',
             'description': 'Перевод организации'},
            {'id': 3598919, 'state': 'EXECUTED', 'date': '2020-12-06T23:00:58Z', 'amount': 29740,
             'currency_name': 'Peso', 'currency_code': 'COP',
             'from': 'Discover 3172601889670065', 'to': 'Discover 0720428384694643',
             'description': 'Перевод с карты на карту'}
        ]
        assert result == expected_result
        mock_read_excel.assert_called_once_with(
            'dummy_path.xlsx')  # Проверяем, что read_excel была вызвана с правильным аргументом


def test_read_transactions_from_excel_file_not_found(capsys):
    # Тест проверки обработки ошибки при отсутствии файла Excel
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = read_transactions_from_excel('non_existent_file.xlsx')  # Вызываем функцию

        assert result == []  # Проверяем, что результат пустой
        captured = capsys.readouterr()  # Считываем вывод в stdout
        # Проверяем, что вывод содержит правильное сообщение об ошибке
        assert "Ошибка: Файл не найден по пути non_existent_file.xlsx" in captured.out


def test_read_transactions_from_excel_general_exception(capsys):
    # Тест проверки обработки общей ошибки при чтении Excel файла
    with patch("pandas.read_excel", side_effect=Exception("Another error")):
        # Вызываем функцию
        result = read_transactions_from_excel('dummy_path.xlsx')

        assert result == []  # Проверяем, что результат пустой
        captured = capsys.readouterr()  # Считываем вывод в stdout
        # Проверяем, что вывод содержит правильное сообщение об ошибке
        assert "Ошибка при чтении Excel-файла: Another error" in captured.out
