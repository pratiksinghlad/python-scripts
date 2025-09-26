"""Composition Example

Demonstrates:
- composing objects to build larger behavior
"""

class Engine:
    def __init__(self, power: int):
        self.power = power

    def start(self):
        return f"Engine started with {self.power} HP"


class Car:
    def __init__(self, make: str, engine: Engine):
        self.make = make
        self.engine = engine  # composition: Car has an Engine

    def start(self):
        return f"{self.make}: {self.engine.start()}"


if __name__ == '__main__':
    print('== Composition Demo ==')
    e = Engine(150)
    c = Car('Toyota', e)
    print(c.start())