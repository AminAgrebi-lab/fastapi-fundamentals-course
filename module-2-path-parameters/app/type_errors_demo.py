"""
This file has intentional type errors for MyPy to catch
"""

def calculate_root(number: int | float) -> float:
    """Calculate square root"""
    return number ** 0.5


# Error 1: Passing string instead of int/float
result1 = calculate_root("25")  # ❌ MyPy will complain

# Error 2: Assigning wrong type to return value
def get_status() -> str:
    return 123  # ❌ MyPy will complain (expected str, got int)


# Error 3: List type mismatch
numbers: list[int] = [1, 2, "three"]  # ❌ MyPy will complain