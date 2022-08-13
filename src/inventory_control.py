from track_orders import TrackOrders


class InventoryControl(TrackOrders):
    INGREDIENTS = {
        "hamburguer": ["pao", "carne", "queijo"],
        "pizza": ["massa", "queijo", "molho"],
        "misto-quente": ["pao", "queijo", "presunto"],
        "coxinha": ["massa", "frango"],
    }
    MINIMUM_INVENTORY = {
        "pao": 50,
        "carne": 50,
        "queijo": 100,
        "molho": 50,
        "presunto": 50,
        "massa": 50,
        "frango": 50,
    }

    def __init__(self):
        self.__orders = list()

        self.__menu = {dish for dish in self.INGREDIENTS.keys()}

        self.__ingredients_for_dish = {
            ingredient: set() for ingredient in self.MINIMUM_INVENTORY.keys()
        }

        for dish, ingredients in self.INGREDIENTS.items():
            for ingredient in ingredients:
                self.__ingredients_for_dish[ingredient].add(dish)

        self.__consumed = dict.fromkeys(self.MINIMUM_INVENTORY.keys(), 0)

    def __update_menu(self) -> None:
        for ingredient, consumed_value in self.__consumed.items():
            if self.MINIMUM_INVENTORY[ingredient] == consumed_value:
                self.__menu = self.__menu.difference(
                    self.__ingredients_for_dish[ingredient]
                )

    def add_new_order(self, customer: str, order: str, day: str) -> None:
        if order not in self.__menu:
            return False

        order_ingredients = self.INGREDIENTS[order]

        for ingredient in order_ingredients:
            self.__consumed[ingredient] += 1

        self.__orders.append(
            {
                "customer": customer,
                "dish": order,
                "weekday": day,
            }
        )
        self.__update_menu()

    def get_quantities_to_buy(self) -> dict:
        return self.__consumed

    def get_available_dishes(self) -> set:
        return self.__menu
