"""OOP Basics Examples

Demonstrates:
- class definition
- instance methods
- class methods
- static methods
- class and instance attributes
- simple usage
"""

class Calculator:
    """Simple calculator demonstrating different method types."""

    factor = 2  # class attribute

    def __init__(self, offset: int = 0):
        self.offset = offset + self.factor  # instance attribute

    def add(self, a: int, b: int) -> int:
        """Instance method: uses instance attributes."""
        return a + b + self.offset

    # Explanation (instance method):
    # - An instance method's first parameter is the instance itself (conventionally `self`).
    # - It can access and modify instance attributes (like `self.offset`) and
    #   also access class attributes via `self.__class__` if needed.
    # - Call it on an instance: `c.add(1, 2)`. Python binds `c` to `self` automatically.
    # - Use instance methods when behavior depends on the particular object's state.

    @classmethod
    def multiply_factor(cls, value: int) -> int:
        """Class method: uses class attribute."""
        return cls.factor * value

    # Explanation (class method):
    # - Decorated with @classmethod. The first parameter is `cls` (the class object).
    # - It receives the class (not an instance), so it can access or modify class-level
    #   state such as `cls.factor`. This is subclass-aware: calling it on a subclass
    #   binds `cls` to that subclass.
    # - Call it on the class or instance: `Calculator.multiply_factor(3)` or `c.multiply_factor(3)`.
    # - Useful for factory methods or operations that belong to the class as a whole.

    @staticmethod
    def subtract(a: int, b: int) -> int:
        """Static method: utility function inside class namespace."""
        return a - b

    # Explanation (static method):
    # - Decorated with @staticmethod. It does NOT receive `self` or `cls`.
    # - Acts like a regular function placed in the class namespace for organizational purposes.
    # - Call it on the class or instance: `Calculator.subtract(10, 4)` or `c.subtract(10, 4)`.
    # - Use static methods for helper utilities that logically belong to the class but
    #   don't need access to class or instance data.

if __name__ == '__main__':
    print('== OOP Basics Demo ==')
    c = Calculator(offset=5)
    print('c.add(10, 3) ->', c.add(10, 3))
    print('Calculator.multiply_factor(3) ->', Calculator.multiply_factor(3))
    print('Calculator.subtract(10, 4) ->', Calculator.subtract(10, 4))
    # Accessing function object on the class
    print('Calculator.add ->', Calculator.add)
    print('Calling unbound: Calculator.add(c, 1, 2) ->', Calculator.add(c, 1, 2))

    # Explanation (bottom usage examples):
    # - c.add(10, 3): demonstrates an instance method — `self` is `c`, so offset is added.
    # - Calculator.multiply_factor(3): demonstrates a class method — uses the class attribute `factor`.
    # - Calculator.subtract(10, 4): demonstrates a static method — simple utility function.
    # - `Calculator.add` prints the function object (unbound function on the class).
    # - `Calculator.add(c, 1, 2)` shows how the instance can be supplied manually; normally Python
    #   does that automatically when you call `c.add(1, 2)`.
