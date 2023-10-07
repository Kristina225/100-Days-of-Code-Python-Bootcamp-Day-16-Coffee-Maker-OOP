import json


class MoneyMachine:
    CURRENCY = "$"
    COIN_VALUES = {
        "quarters": 0.25,
        "dimes": 0.10,
        "nickles": 0.05
    }

    def __init__(self):
        self.profit = self._get_profit()
        self.transaction_coins = {
            "quarters": 0,
            "nickles": 0,
            "dimes": 0
        }
        self.transaction_total = 0

    @staticmethod
    def _get_profit() -> float:
        """Returns the profit made by the coffee maker"""
        with open("available_money.json", "r") as file:
            money = json.load(file)
        return money["profit"]

    def report(self) -> None:
        """Issues a report of the profit made by the coffee maker"""
        print(f"Money: {self.profit}{MoneyMachine.CURRENCY}")

    def _process_coins(self) -> None:
        """Asks user to insert coins in the machine and calculates the transaction total"""
        for coin, value in MoneyMachine.COIN_VALUES.items():
            while True:
                inserted_coins = input(f"How many {coin} will you be inserting: ")
                try:
                    inserted_coins = int(inserted_coins)
                except ValueError:
                    print("Sorry, that's not real money.")
                else:
                    break
            self.transaction_coins[coin] = inserted_coins
        for coin, quantity in self.transaction_coins.items():
            self.transaction_total += quantity * MoneyMachine.COIN_VALUES[coin]

    def _check_transaction(self, cost: float) -> str:
        """Checks the cost of the drink against the entered amount by the user and asks user if they
        wish to continue or cancel their order"""
        print(self.transaction_total)
        if self.transaction_total < cost:
            continue_transaction = input(f"You're sill missing: {self.transaction_total - cost}{MoneyMachine.CURRENCY}.\n"
                                    f"Enter 'yes' to add more coins, 'no' to cancel: ").lower()
            return continue_transaction
        else:
            return "done"

    def _add_money(self, cost: float) -> None:
        """Adds coins entered by the user to the coffee maker"""
        with open("available_money.json", "r") as file:
            available_coins = json.load(file)
        for coin, quantity in self.transaction_coins.items():
            available_coins["coins"][coin] += quantity
        available_coins["profit"] += cost
        with open("available_money.json", "w") as file:
            json.dump(available_coins, file)

    @staticmethod
    def _remove_money(change: float) -> None:
        """Removes money from the coffee maker to return as change to the user"""
        change_left = change
        deducted_coins = {}
        with open("available_money.json", "r") as file:
            available_coins = json.load(file)
        for coin, quantity in available_coins["coins"].items():
            deducted_coins[coin] = 0
            while quantity > 0 and change_left > MoneyMachine.COIN_VALUES[coin]:
                change_left -= MoneyMachine.COIN_VALUES[coin]
                deducted_coins[coin] += 1
                available_coins["coins"][coin] -= 1
        with open("available_money.json", "w") as file:
            json.dump(available_coins, file)

    def _reset_current_transaction(self) -> None:
        """Resets temporary values used for the current transaction to zero"""
        self.transaction_coins = {
            "quarters": 0,
            "nickles": 0,
            "dimes": 0
        }
        self.transaction_total = 0

    def make_payment(self, cost: float) -> bool:
        """Manages the payment process for the chosen drink by the user.
        Returns True if the transaction is successful, False otherwise."""
        while True:
            self._process_coins()
            continue_transaction = self._check_transaction(cost)
            if continue_transaction == "done":
                break
            elif continue_transaction == "yes":
                continue
            elif continue_transaction == "no":
                print(f"Your order was canceled. Here's your money back: {self.transaction_total}")
                self._reset_current_transaction()
                return False
        change = self.transaction_total - cost

        print(f"Thank you for your order. Here's your change {round(change, 2)}{MoneyMachine.CURRENCY}")
        self._add_money(cost)
        self._remove_money(change)
        self._reset_current_transaction()
        return True
