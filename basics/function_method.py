# function_method.py
from typing import Callable

# -------------------------
# Module-level function
# -------------------------
def multiply(x: int, y: int) -> int:
    """Simple module-level function (not bound to any class)."""
    return x * y


# -------------------------
# Nested function / closure
# -------------------------
def make_power_function(exp: int) -> Callable[[int], int]:
    """
    Demonstrates a function defined inside another function.
    Returns a function that raises its input to the given exponent.
    The inner function closes over `exp`.
    """
    def power(base: int) -> int:
        # 'power' is a nested function that can access 'exp' from the outer scope
        return base ** exp

    return power  # return the inner function (a closure)


# -------------------------
# Class with different method types
# -------------------------
class MathUtils:
    """Class demonstrating instance, class, and static methods."""

    factor = 10  # class attribute

    def __init__(self, offset: int = 0):
        self.offset = offset  # instance attribute

    # Instance method: receives the instance as 'self'
    def add(self, a: int, b: int) -> int:
        """Instance method: can use instance attributes."""
        return a + b + self.offset

    # Class method: receives the class as 'cls'
    @classmethod
    def scaled_factor(cls) -> int:
        """Class method: can access/modify class-level data."""
        return cls.factor * 2

    # Static method: doesn't receive instance or class automatically
    @staticmethod
    def subtract(a: int, b: int) -> int:
        """Static method: just a function placed in the class namespace."""
        return a - b


# -------------------------
# Demonstration / tests
# -------------------------
if __name__ == "__main__":
    print("== Module-level function ==")
    print("multiply(3, 4) ->", multiply(3, 4))  # 12

    print("\n== Nested function / closure ==")
    square = make_power_function(2)   # returns a function that squares its input
    cube = make_power_function(3)     # returns a function that cubes its input
    print("square(5) ->", square(5))  # 25
    print("cube(2) ->", cube(2))      # 8

    # Show that the nested function retained 'exp' (closure)
    for f, n in [(square, 4), (cube, 3)]:
        print(f"f({n}) ->", f(n))

    print("\n== Methods on an object ==")
    mu = MathUtils(offset=7)
    print("mu.add(10, 5) ->", mu.add(10, 5))  # 10 + 5 + offset(7) = 22

    print("\n== Class method and static method ==")
    print("MathUtils.scaled_factor() ->", MathUtils.scaled_factor())  # uses class attribute
    print("MathUtils.subtract(10, 3) ->", MathUtils.subtract(10, 3))  # 7

    # You can also call the class method and static method via an instance:
    print("mu.scaled_factor() ->", mu.scaled_factor())
    print("mu.subtract(9, 1) ->", mu.subtract(9, 1))

    print("\n== Low-level view: methods are functions stored on the class ==")
    # Accessing the function object directly from the class:
    print("MathUtils.add (raw function on class) ->", MathUtils.add)        # function object
    # Calling the function by passing the instance explicitly (unbound style)
    print("MathUtils.add(mu, 1, 2) ->", MathUtils.add(mu, 1, 2))          # same as mu.add(1, 2)
