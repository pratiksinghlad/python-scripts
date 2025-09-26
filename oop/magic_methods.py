"""Magic (dunder) Methods Example

Demonstrates:
- __str__, __repr__, __add__, __len__, comparison methods
"""

class Vector:
    def __init__(self, *components):
        self.components = list(components)

    def __len__(self):
        return len(self.components)

    def __str__(self):
        return f"Vector({', '.join(map(str, self.components))})"

    def __repr__(self):
        return f"Vector({self.components})"

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        # add component-wise, pad with zeros
        max_len = max(len(self), len(other))
        a = self.components + [0] * (max_len - len(self))
        b = other.components + [0] * (max_len - len(other))
        return Vector(*[x + y for x, y in zip(a, b)])

    def __eq__(self, other):
        return isinstance(other, Vector) and self.components == other.components


if __name__ == '__main__':
    print('== Magic Methods Demo ==')
    v1 = Vector(1, 2)
    v2 = Vector(3, 4, 5)
    print('v1 ->', v1)
    print('v2 ->', v2)
    print('v1 + v2 ->', v1 + v2)
    print('len(v2) ->', len(v2))
    print('v1 == Vector(1,2) ->', v1 == Vector(1, 2))