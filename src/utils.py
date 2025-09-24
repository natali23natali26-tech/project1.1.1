import json
import os


def load_transactions(file_path):
    """
    Загружает финансовые транзакции из указанного JSON-файла.

    :param file_path: Путь до JSON-файла
    :return: Список словарей с данными о транзакциях или пустой список, если
             файл пустой, не найден или имеет неправильный формат
    """
    # Проверяем, существует ли файл по указанному пути
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return []

    # Попробуем открыть и прочитать файл
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON. Проверьте формат файла.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

    # Проверяем, является ли прочитанные данные списком
    if not isinstance(data, list):
        print("Данные в файле не представляют собой список.")
        return []

    return data
