import pytest
import logging

# Импортируем декоратор, который мы тестируем
from src.decorators import log


@log()
def add(x, y):
    return x + y


@log()
def divide(x, y):
    return x / y


# Фикстура для настройки захвата логирования
@pytest.fixture(autouse=True)
def caplog_fixture(caplog):
    # Установим уровень логирования на INFO
    caplog.set_level(logging.INFO)
    return caplog


def test_addition(caplog):
    # Тестируем успешное выполнение функции сложения
    with caplog.at_level(logging.INFO):
        result = add(1, 2)

    # Проверяем результат
    assert result == 3

    # Проверяем вывод логов
    assert "Start execution of add with args: (1, 2) and kwargs: {}" in caplog.text
    assert "add ok; result: 3" in caplog.text


def test_division(caplog):
    # Тестируем успешное выполнение функции деления
    with caplog.at_level(logging.INFO):
        result = divide(10, 2)

    # Проверяем результат
    assert result == 5

    # Проверяем вывод логов
    assert "Start execution of divide with args: (10, 2) and kwargs: {}" in caplog.text
    assert "divide ok; result: 5" in caplog.text


def test_divide_by_zero(caplog):
    # Тестируем деление на ноль, которое вызовет исключение
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

    # Проверяем, что исключение было вызвано
    pass
