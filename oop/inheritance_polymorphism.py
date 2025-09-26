"""Inheritance and Polymorphism Examples

Demonstrates:
- base class with a method
- derived classes overriding methods
- polymorphic behavior via a function that accepts base-class typed objects
"""

class Animal:
    def speak(self) -> str:
        return "..."


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


def animal_says(animal: Animal):
    print(f"Animal says: {animal.speak()}")


if __name__ == '__main__':
    print('== Inheritance & Polymorphism Demo ==')
    animals = [Dog(), Cat(), Animal()]
    for a in animals:
        animal_says(a)