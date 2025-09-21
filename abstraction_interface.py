"""Abstraction / Interface Example

Demonstrates:
- abstract base class with abstract methods
- concrete implementations
"""
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


if __name__ == '__main__':
    print('== Abstraction / Interface Demo ==')
    r = Rectangle(3, 4)
    print('Area:', r.area())
    print('Perimeter:', r.perimeter())