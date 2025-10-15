import re
from collections import Counter
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Функция для поиска банковских операций по описанию.

    Args:
        data (List[Dict]): Список словарей с данными о банковских операциях.
        search (str): Строка поиска.

    Returns:
        List[Dict]: Список словарей, у которых в описании есть строка поиска.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [transaction for transaction in data if pattern.search(transaction['description'])]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Функция для подсчета количества банковских операций по категориям.

    Args:
        data (List[Dict]): Список словарей с данными о банковских операциях.
        categories (List[str]): Список категорий операций.

    Returns:
        Dict[str, int]: Словарь с количеством операций в каждой категории.
    """
    category_counts = Counter()

    for transaction in data:
        description = transaction['description']
        for category in categories:
            if category.lower() in description.lower():
                category_counts[category] += 1

    return dict(category_counts)
