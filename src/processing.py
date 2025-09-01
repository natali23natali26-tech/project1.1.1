def filter_by_state(data, state='EXECUTED'):
    """
    Фильтрует список словарей, оставляя только те, у которых значение ключа 'state'
    соответствует указанному значению (по умолчанию 'EXECUTED').

    Args:
        data (list): Список словарей.
        state (str, optional): Значение ключа 'state' для фильтрации.
            По умолчанию 'EXECUTED'.

    Returns:
        list: Новый список словарей, содержащий только те словари, у которых
            ключ 'state' соответствует указанному значению.
    """
    filtered_data = [item for item in data if item.get('state') == state]
    return filtered_data


if __name__ == '__main__':
    data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    executed_data = filter_by_state(data)
    print("Выход функции со статусом по умолчанию 'EXECUTED':")
    print(executed_data)

    canceled_data = filter_by_state(data, 'CANCELED')
    print("\nВыход функции, если вторым аргументов передано 'CANCELED':")
    print(canceled_data)