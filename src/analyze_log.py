import csv
from typing import List, Dict


def open_file(path_to_file: str) -> List[Dict[str, str]]:
    if not path_to_file.strip().lower().endswith('.csv'):
        raise FileNotFoundError(f"Extensão inválida: {path_to_file}")

    try:
        with open(path_to_file, 'r', encoding='utf8') as file:
            fd = ['customer', 'dish', 'weekday']
            return list(csv.DictReader(file, fieldnames=fd, delimiter=','))

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo inexistente: {path_to_file}")


def write_report(path_to_file: str, report: dict) -> None:
    with open(path_to_file, 'w', encoding='utf-8') as file:
        report = (
            f"{report['dish']}\n"
            + f"{report['order_quantity']}\n"
            + f"{report['dishes']}\n"
            + f"{report['weekdays']}\n"
        )
        file.write(report)


def get_open_days(orders: list) -> set:
    return {order['weekday'] for order in orders}


def get_customers(orders: list) -> set:
    return {order['customer'] for order in orders}


def get_menu(orders: list) -> set:
    return {order['dish'] for order in orders}


def get_most_ordered_dish_per_customer(orders: list, customer: str) -> str:
    menu = dict.fromkeys(get_menu(orders), 0)
    count = 0
    for order in orders:
        if customer == order['customer']:
            menu[order['dish']] += 1
            if menu[order['dish']] > count:
                count = menu[order['dish']]
                dish = order['dish']
    return dish


def get_how_many_times_a_customer_ordered_a_dish(
        orders: list, customer: str, dish: str) -> int:
    menu = dict.fromkeys(get_menu(orders), 0)

    for order in orders:
        if customer == order['customer']:
            menu[order['dish']] += 1
    return menu[dish]


def get_which_dishes_a_customer_has_never_ordered(
        orders: list, customer: str) -> set:
    menu = get_menu(orders)
    customer_menu = {
        order['dish'] for order in orders if order['customer'] == customer
    }
    return menu.difference(customer_menu)


def get_which_days_a_customer_never_went_to_the_diner(
        orders: list, customer: str) -> set:
    opened_days = get_open_days(orders)
    visited_days = {
        order['weekday'] for order in orders if order['customer'] == customer
    }
    return opened_days.difference(visited_days)


def analyze_log(path_to_file: str) -> None:
    orders = open_file(path_to_file)

    dish = get_most_ordered_dish_per_customer(
        orders, 'maria')

    order_quantity = get_how_many_times_a_customer_ordered_a_dish(
        orders, 'arnaldo', 'hamburguer')

    dishes = get_which_dishes_a_customer_has_never_ordered(
        orders, 'joao')

    weekdays = get_which_days_a_customer_never_went_to_the_diner(
        orders, 'joao')

    report = {
        'dish': dish,
        'order_quantity': order_quantity,
        'dishes': dishes,
        'weekdays': weekdays}

    write_report('data/mkt_campaign.txt', report)
