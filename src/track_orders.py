class TrackOrders:
    def __init__(self):
        self.__orders = list()

    def __len__(self) -> int:
        return len(self.__orders)

    def add_new_order(self, customer: str, order: str, day: str):
        self.__orders.append({
            'customer': customer,
            'dish': order,
            'weekday': day,
        })

    def __get_customers(self) -> set:
        return {order['customer'] for order in self.__orders}

    def __get_menu(self) -> set:
        return {order['dish'] for order in self.__orders}

    def __get_open_days(self) -> set:
        return {order['weekday'] for order in self.__orders}

    def get_most_ordered_dish_per_customer(self, customer: str) -> str:
        menu = dict.fromkeys(self.__get_menu(), 0)
        count = 0

        for order in self.__orders:
            if customer == order['customer']:
                menu[order['dish']] += 1
                if menu[order['dish']] > count:
                    count = menu[order['dish']]
                    dish = order['dish']

        return dish

    def get_never_ordered_per_customer(self, customer: str) -> set:
        menu = self.__get_menu()

        customer_menu = {
            order['dish']
            for order in self.__orders
            if order['customer'] == customer
        }

        return menu.difference(customer_menu)

    def get_days_never_visited_per_customer(self, customer: str) -> set:
        opened_days = self.__get_open_days()

        visited_days = {
            order['weekday']
            for order in self.__orders
            if order['customer'] == customer
        }

        return opened_days.difference(visited_days)

    def get_busiest_day(self) -> str:
        opened_days = dict.fromkeys(self.__get_open_days(), 0)
        max_count = 0

        for order in self.__orders:
            opened_days[order['weekday']] += 1

        for day, day_count in opened_days.items():
            if day_count > max_count:
                max_count = day_count
                busiest_day = day

        return busiest_day

    def get_least_busy_day(self):
        opened_days = dict.fromkeys(self.__get_open_days(), 0)
        min_count = len(self.__orders)

        for order in self.__orders:
            opened_days[order['weekday']] += 1

        for day, day_count in opened_days.items():
            if day_count < min_count:
                min_count = day_count
                least_day = day

        return least_day
