import pytest
from unittest.mock import patch
import pandas as pd
from io import StringIO
from src.read_csv_and_exel import read_transactions_from_csv, read_transactions_from_excel

def test_read_transactions_from_csv_success():
    with patch("pandas.read_csv") as mock_read_csv:
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_read_csv.return_value = mock_df

        result = read_transactions_from_csv('dummy_path.csv')

        assert result == [{'col1': 1, 'col2': 3}, {'col1': 2, 'col2': 4}]
        mock_read_csv.assert_called_once_with('dummy_path.csv')

def test_read_transactions_from_csv_file_not_found(capsys):
    with patch("pandas.read_csv", side_effect=FileNotFoundError):
        result = read_transactions_from_csv('non_existent_file.csv')

        assert result == []
        captured = capsys.readouterr()
        assert "Ошибка: Файл не найден по пути non_existent_file.csv" in captured.out

def test_read_transactions_from_csv_general_exception(capsys):
    with patch("pandas.read_csv", side_effect=Exception("Some error")):
        result = read_transactions_from_csv('dummy_path.csv')

        assert result == []
        captured = capsys.readouterr()
        assert "Ошибка при чтении CSV-файла: Some error" in captured.out

def test_read_transactions_from_excel_success():
    with patch("pandas.read_excel") as mock_read_excel:
        mock_df = pd.DataFrame({'col1': [5, 6], 'col2': [7, 8]})
        mock_read_excel.return_value = mock_df
        result = read_transactions_from_excel('dummy_path.xlsx')

        assert result == [{'col1': 5, 'col2': 7}, {'col1': 6, 'col2': 8}]
        mock_read_excel.assert_called_once_with('dummy_path.xlsx')

def test_read_transactions_from_excel_file_not_found(capsys):
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = read_transactions_from_excel('non_existent_file.xlsx')

        assert result == []
        captured = capsys.readouterr()
        assert "Ошибка: Файл не найден по пути non_existent_file.xlsx" in captured.out

def test_read_transactions_from_excel_general_exception(capsys):
    with patch("pandas.read_excel", side_effect=Exception("Another error")):
        # Call the function
        result = read_transactions_from_excel('dummy_path.xlsx')

        assert result == []
        captured = capsys.readouterr()
        assert "Ошибка при чтении Excel-файла: Another error" in captured.out
