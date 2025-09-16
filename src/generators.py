def filter_by_currency(transactions, currency_code):
    """Фильтрует транзакции по заданной валюте и возвращает итератор."""
    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == currency_code:
            yield transaction

def transaction_descriptions(transactions):
    """Генерирует описания транзакций."""
    for transaction in transactions:
        yield transaction['description']

def card_number_generator(start, stop):
    """Генерирует номера банковских карт в заданном диапазоне."""
    for num in range(start, stop + 1):
        yield f"{num:016d}"[:4] + " " + f"{num:016d}"[4:8] + " " + f"{num:016d}"[8:12] + " " + f"{num:016d}"[12:16]
