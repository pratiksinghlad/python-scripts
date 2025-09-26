"""Encapsulation Example

Demonstrates:
- private attributes (name mangling)
- property getters/setters
- controlled access to internal state
"""

class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.__balance = float(balance)  # private attribute

    @property
    def balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError('Deposit amount must be positive')
        self.__balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError('Withdrawal amount must be positive')
        if amount > self.__balance:
            raise ValueError('Insufficient funds')
        self.__balance -= amount


if __name__ == '__main__':
    print('== Encapsulation Demo ==')
    acct = BankAccount('Alice', 100.0)
    print('Owner:', acct.owner)
    print('Initial balance:', acct.balance)
    acct.deposit(50)
    print('After deposit:', acct.balance)
    try:
        acct.withdraw(200)
    except ValueError as e:
        print('Withdraw failed:', e)