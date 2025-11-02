"""
Demonstrates Python data types and variable declarations with type hints.
Shows built-in types, custom types, collections, and type annotations.
"""
from typing import List, Dict, Tuple, Set, Optional, Union, Any
from decimal import Decimal
from datetime import datetime, date

# Basic Types
# -------------------------
name: str = "John Doe"
age: int = 30
height: float = 5.11
is_active: bool = True
salary: Decimal = Decimal("75000.50")  # More precise than float for money

# None and Optional Types
# -------------------------
user_id: Optional[int] = None  # Can be int or None
status: Union[int, str] = "active"  # Can be int or str
dynamic_value: Any = 42  # Can be any type

# Sequence Types
# -------------------------
# List (mutable sequence)
numbers: List[int] = [1, 2, 3, 4, 5]
names: List[str] = ["Alice", "Bob", "Charlie"]
mixed_list: List[Union[int, str]] = [1, "two", 3, "four"]

# Tuple (immutable sequence)
coordinates: Tuple[float, float] = (40.7128, -74.0060)  # Latitude, Longitude
rgb_color: Tuple[int, int, int] = (255, 128, 0)  # RGB values

# Set Types (unique elements)
# -------------------------
unique_numbers: Set[int] = {1, 2, 3, 3, 4}  # Duplicates removed automatically
tags: Set[str] = {"python", "programming", "coding"}

# Dictionary Types
# -------------------------
person: Dict[str, Union[str, int]] = {
    "name": "Jane Doe",
    "age": 28,
    "city": "New York"
}

config: Dict[str, Any] = {
    "debug": True,
    "max_connections": 100,
    "server_name": "prod-01"
}

# Date and Time Types
# -------------------------
current_date: date = date.today()
current_time: datetime = datetime.now()
timestamp: float = datetime.now().timestamp()

# Custom Type Aliases
# -------------------------
UserId = int
UserName = str

def get_user(user_id: UserId, name: UserName) -> Dict[str, Union[int, str]]:
    """Example function using custom type aliases."""
    return {"id": user_id, "name": name}

# Complex Data Structures
# -------------------------
# List of dictionaries
users: List[Dict[str, Union[int, str]]] = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

# Dictionary with tuple keys
matrix: Dict[Tuple[int, int], float] = {
    (0, 0): 1.0,
    (0, 1): 0.5,
    (1, 0): 0.5,
    (1, 1): 1.0
}

def main() -> None:
    """Demonstrate the usage of different data types."""
    # Print basic types
    print(f"Name: {name} (type: {type(name)})")
    print(f"Age: {age} (type: {type(age)})")
    print(f"Height: {height} (type: {type(height)})")
    print(f"Is Active: {is_active} (type: {type(is_active)})")
    print(f"Salary: {salary} (type: {type(salary)})")
    
    # Print sequence operations
    print("\nSequence Operations:")
    print(f"First number: {numbers[0]}")
    print(f"Last name: {names[-1]}")
    print(f"Coordinates: Lat={coordinates[0]}, Long={coordinates[1]}")
    
    # Print set operations
    print("\nSet Operations:")
    print(f"Unique numbers: {unique_numbers}")
    print(f"Number of tags: {len(tags)}")
    
    # Print dictionary access
    print("\nDictionary Access:")
    print(f"Person's name: {person['name']}")
    print(f"Server name: {config['server_name']}")
    
    # Print date/time
    print("\nDate and Time:")
    print(f"Current date: {current_date}")
    print(f"Current time: {current_time}")
    
    # Use custom type function
    user_info = get_user(UserId(1), UserName("Alice"))
    print("\nCustom Types:")
    print(f"User info: {user_info}")
    
    # Demonstrate type checking
    try:
        numbers.append("not a number")  # This would raise a type error in a type checker
    except TypeError as e:
        print(f"\nType Error: {e}")

if __name__ == "__main__":
    main()