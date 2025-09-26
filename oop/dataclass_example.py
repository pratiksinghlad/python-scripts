"""Dataclass Example

Demonstrates:
- Python's @dataclass usage
- default values and immutability (frozen)
"""
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int = 0


@dataclass(frozen=True)
class Point:
    x: float
    y: float


if __name__ == '__main__':
    print('== Dataclass Demo ==')
    p = Person('Bob', 30)
    print(p)
    pt = Point(1.0, 2.0)
    print('Point:', pt)
    try:
        pt.x = 5.0
    except Exception as e:
        print('Cannot modify frozen dataclass:', e)