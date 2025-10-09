import pandas as pd


def read_transactions_from_csv(csv_path):
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        csv_path (str): Путь к CSV-файлу.

    Returns:
        list: Список словарей с транзакциями.
    """
    try:
        df = pd.read_csv(csv_path)  # Читаем данные из CSV файла в DataFrame
        transactions = df.to_dict(orient='records')  # Преобразуем DataFrame в список словарей
        return transactions
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути {csv_path}")  # Обрабатываем ошибку, если файл не найден
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV-файла: {e}")  # Обрабатываем любые другие исключения
        return []


def read_transactions_from_excel(excel_path):
    """
    Считывает финансовые операции из Excel-файла.

    Args:
        excel_path (str): Путь к Excel-файлу.

    Returns:
        list: Список словарей с транзакциями.
    """
    try:
        df = pd.read_excel(excel_path)  # Читаем данные из Excel файла в DataFrame
        transactions = df.to_dict(orient='records')  # Преобразуем DataFrame в список словарей
        return transactions  # Возвращаем список транзакций
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути {excel_path}")  # Обрабатываем ошибку, если файл не найден
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel-файла: {e}")  # Обрабатываем любые другие исключения
        return []


if __name__ == '__main__':
    # Указываем пути к файлам CSV и Excel
    csv_file_path = r"C:\Users\nata6\PycharmProjects\my_prg\Client's personal account\data\transactions.csv"
    excel_file_path = r"C:\Users\nata6\PycharmProjects\my_prg\Client's personal account\data\transactions_excel.xlsx"

    # Читаем транзакции из файлов
    csv_transactions = read_transactions_from_csv(csv_file_path)  # Чтение из CSV
    excel_transactions = read_transactions_from_excel(excel_file_path)  # Чтение из Excel

    print("Транзакции из CSV:")
    for transaction in csv_transactions:
        print(transaction)

    print("\nТранзакции из Excel:")
    for transaction in excel_transactions:
        print(transaction)
