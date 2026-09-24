"""
Type Hinting in Python - Comprehensive Examples
Based on Module 2: Type Hinting lesson
"""

# ============================================
# 1. Basic Type Hints for Variables
# ============================================

# Simple types
text: str = "Hello FastAPI"
number: int = 42
percentage: float = 95.5
is_active: bool = True
file_data: bytes = b"binary data"

print(f"Text: {text}")
print(f"Number: {number}")
print(f"Percentage: {percentage}")

# ============================================
# 2. Type Hints for Functions
# ============================================

def calculate_root(number: int) -> float:
    """
    Calculate the square root of a number
    
    Args:
        number (int): The number to calculate root for
    
    Returns:
        float: The square root
    """
    return number ** 0.5


# Test the function
result = calculate_root(25)
print(f"\nRoot of 25: {result}")  # Output: 5.0

# ============================================
# 3. Union Types (Multiple Possible Types)
# ============================================

# Using pipe operator (|) - Python 3.10+
flexible_number: int | float = 10
flexible_number = 10.5  # Also valid!

def process_number(value: int | float) -> float:
    """Accept both int and float"""
    return float(value) ** 0.5


print(f"\nProcess 16: {process_number(16)}")      # 4.0
print(f"Process 15.5: {process_number(15.5)}")    # 3.937...

# ============================================
# 4. Optional Values (Can be None)
# ============================================

# Value can be string or None
optional_value: str | None = None
optional_value = "Now it has a value"

# In functions with default values
def calculate_power(base: float, exponent: float | None = None) -> float:
    """
    Calculate power with optional exponent
    
    If exponent is None, defaults to 0.5 (square root)
    """
    # Using ternary operator
    exp = 0.5 if exponent is None else exponent
    return base ** exp


print(f"\nPower(16) with default: {calculate_power(16)}")        # 4.0
print(f"Power(2, 3): {calculate_power(2, 3)}")                   # 8.0
print(f"Power(9, None): {calculate_power(9, None)}")             # 3.0

# ============================================
# 5. Sequence Types (List, Tuple, Dict)
# ============================================

# List - mutable, variable length
digits: list[int] = [1, 2, 3, 4, 5]
digits.append(6)  # Valid - lists are mutable
print(f"\nDigits list: {digits}")

# Tuple - immutable, can have fixed or variable length
# Variable length tuple (unknown number of elements)
temperatures: tuple[int, ...] = (20, 22, 25, 23, 21)
print(f"Temperatures: {temperatures}")

# Fixed length tuple (known number of elements with specific types)
city_temp: tuple[str, float] = ("Cairo", 35.5)
print(f"City temp: {city_temp}")

# Dictionary - key-value pairs
shipment: dict[str, any] = {
    "content": "wooden table",
    "status": "in transit",
    "id": 123,
    "weight": 15.5
}
print(f"\nShipment: {shipment}")

# More specific dictionary (keys: str, values: str or int)
simple_shipment: dict[str, str | int] = {
    "content": "wooden table",
    "status": "in transit",
    "id": 123
}
print(f"Simple shipment: {simple_shipment}")

# ============================================
# 6. Custom Classes as Type Hints
# ============================================

class City:
    """Custom City class"""
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
    
    def __str__(self):
        return f"{self.name} ({self.location})"


# Using custom class as type hint
city_data: tuple[City, float] = (
    City("Hampshire", "UK"),
    18.5
)

print(f"\nCity data: {city_data[0]}, Temp: {city_data[1]}°C")

# ============================================
# 7. Real-World Example: Shipment Model
# ============================================

class Shipment:
    """Real-world example combining all concepts"""
    
    def __init__(
        self,
        id: int,
        content: str,
        status: str,
        weight: float | None = None,
        tags: list[str] | None = None
    ):
        self.id = id
        self.content = content
        self.status = status
        self.weight = weight
        self.tags = tags or []  # Default to empty list if None
    
    def get_summary(self) -> dict[str, any]:
        """Return shipment summary as dictionary"""
        return {
            "id": self.id,
            "content": self.content,
            "status": self.status,
            "weight": self.weight,
            "tags": self.tags
        }


# Create shipment instance
my_shipment = Shipment(
    id=1,
    content="wooden table",
    status="in transit",
    weight=15.5,
    tags=["fragile", "furniture"]
)

print("\n" + "="*50)
print("Shipment Summary:")
print("="*50)
for key, value in my_shipment.get_summary().items():
    print(f"{key}: {value}")