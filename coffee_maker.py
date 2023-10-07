import json
import sys
from menu import Menu, MenuItem
from money_machine import MoneyMachine


class CoffeeMaker:
    def __init__(self):
        self.menu = Menu()
        self.money_machine = MoneyMachine()

    @staticmethod
    def _make_coffee(drink: MenuItem) -> None:
        """Deducts ingredients used to make a drink, and prints a message to user when done"""
        with open("available_ingredients.json", "r") as file:
            available_ingredients = json.load(file)
        for ingredient, quantity in drink.ingredients.items():
            available_ingredients[ingredient] -= quantity
        with open("available_ingredients.json", "w") as file:
            json.dump(available_ingredients, file)
        print(f"Here's your {drink.name} ☕️. Enjoy!")

    @staticmethod
    def _report_ingredients() -> None:
        """Prints a report of all available ingredients"""
        with open("available_ingredients.json", "r") as file:
            ingredients = json.load(file)
        for ingredient, quantity in ingredients.items():
            ingredient_name, ingredient_unit = ingredient.split("_")
            print(f"{ingredient_name.capitalize()}: {quantity} {ingredient_unit.lower()}")

    def run_machine(self) -> None:
        """Takes user input from available coffee choices, then either prints a report or makes a coffee"""
        while True:
            available_drinks = self.menu.get_menu()
            if not available_drinks:
                print("Coffee Maker is out of order. Please come back later!")
                sys.exit()
            user_input = input(f"What would you like to drink. We have {', '.join(available_drinks)}: ").lower()
            if user_input == "report":
                self._report_ingredients()
                self.money_machine.report()
                continue
            drink = self.menu.find_menu_item(user_input)
            if not drink:
                print("Sorry, we don't serve that.")
                continue
            payment_successful = self.money_machine.make_payment(drink.price)
            if payment_successful:
                self._make_coffee(drink)
