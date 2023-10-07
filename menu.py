import json


class MenuItem:
    def __init__(self, name, price, ingredients):
        self.name = name
        self.price = price
        self.ingredients = ingredients


class Menu:
    def __init__(self):
        self.menu: list = self._get_menu_items()

    @staticmethod
    def _get_menu_items() -> list[MenuItem]:
        """Returns a list of MenuItem objects representing the drinks that the machine is capable of making"""
        with open("menu_items.json", "r") as file:
            menu_items = json.load(file)
        menu_items_list = []
        for item_name, props in menu_items.items():
            menu_item = MenuItem(name=item_name, price=props["price_USD"], ingredients=props["ingredients"])
            menu_items_list.append(menu_item)
        return menu_items_list

    def get_menu(self) -> list[str]:
        """Returns a list of the drinks items names after checking if there are enough ingredients to prepare them"""
        with open("available_ingredients.json", "r") as file:
            available_ingredients = json.load(file)
        available_menu_items_names = set()
        for menu_item in self.menu:
            available_menu_items_names.add(menu_item.name)
            for ingredient, quantity in menu_item.ingredients.items():
                if quantity > available_ingredients[ingredient]:
                    available_menu_items_names.discard(menu_item.name)
        return sorted(available_menu_items_names)

    def find_menu_item(self, menu_item_name: str) -> MenuItem or None:
        """Returns a MenuItem object from Menu list or None"""
        for menu_item in self.menu:
            if menu_item.name == menu_item_name:
                return menu_item
        else:
            return False
