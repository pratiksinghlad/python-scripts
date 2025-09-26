"""Exceptions Example

Demonstrates custom exceptions and using them in classes
"""

class InsufficientFundsError(Exception):
    pass


class Wallet:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance

    def spend(self, amount: float):
        if amount > self.balance:
            raise InsufficientFundsError(f"Not enough funds to spend {amount}")
        self.balance -= amount

    def spending(self,amount: float):
        print(f"Spending {amount}")  


if __name__ == '__main__':
    print('== Exceptions Demo ==')
    w = Wallet('Sam', 20)
    w.spending(10)
    try:
        w.spend(30)
    except InsufficientFundsError as e:
        print('Failed to spend:', e)