"""
Function Decorators in Python - Step by Step
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

# ============================================
# 1. Basic Decorator (No Arguments)
# ============================================

def fence_decorator(func):
    """
    A simple decorator that adds fences around function output
    """
    def wrapper():
        print("+" * 10)  # Top fence
        func()           # Call the original function
        print("+" * 10)  # Bottom fence
    
    return wrapper


# Using the decorator
@fence_decorator
def log_message():
    print("Decorated!")


# Test it
print("=" * 50)
print("Example 1: Basic Decorator")
print("=" * 50)
log_message()

# ============================================
# 2. Understanding How Decorators Work
# ============================================

print("\n" + "=" * 50)
print("Example 2: How Decorators Work Internally")
print("=" * 50)

# This is what happens when you use @decorator:
# @fence_decorator
# def log_message():
#     print("Decorated!")

# Is equivalent to:
def log_message_original():
    print("Decorated!")

# Python does this automatically:
log_message_decorated = fence_decorator(log_message_original)

# Now when you call it:
log_message_decorated()

# ============================================
# 3. Decorator with Arguments
# ============================================

def custom_fence(fence_char="+"):
    """
    A decorator factory that accepts arguments
    """
    def decorator(func):
        def wrapper():
            print(fence_char * 10)  # Custom fence
            func()
            print(fence_char * 10)
        return wrapper
    return decorator


# Using the decorator with arguments
@custom_fence("-")
def log_with_dashes():
    print("Dashes around me!")


@custom_fence("*")
def log_with_stars():
    print("Stars around me!")


print("\n" + "=" * 50)
print("Example 3: Decorator with Arguments")
print("=" * 50)
log_with_dashes()
print()
log_with_stars()

# ============================================
# 4. Decorator for Functions with Arguments
# ============================================

def log_execution(func):
    """
    Decorator that logs function execution
    """
    @wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper


@log_execution
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@log_execution
def greet(name: str, greeting: str = "Hello") -> str:
    """Greet a person"""
    return f"{greeting}, {name}!"


print("\n" + "=" * 50)
print("Example 4: Decorator for Functions with Arguments")
print("=" * 50)
result1 = add(5, 3)
print(f"Final result: {result1}\n")

result2 = greet("Ahmed", greeting="Welcome")
print(f"Final result: {result2}")

# ============================================
# 5. Type Hinting for Decorators
# ============================================

def typed_decorator(func: Callable[[int, int], int]) -> Callable[[], int]:
    """
    Decorator with type hints
    - func: Callable that takes two ints and returns an int
    - returns: Callable that takes no args and returns an int
    """
    def wrapper() -> int:
        print("Executing typed function...")
        return func(10, 20)
    return wrapper


@typed_decorator
def multiply(a: int, b: int) -> int:
    return a * b


print("\n" + "=" * 50)
print("Example 5: Type Hinting for Decorators")
print("=" * 50)
result = multiply()
print(f"Result: {result}")

# ============================================
# 6. Simulating FastAPI's Routing System
# ============================================

# Dictionary to store routes (like FastAPI does internally)
routes: dict[str, Callable[[], Any]] = {}


def route(path: str):
    """
    Decorator that registers a function as a route handler
    This is similar to how @app.get() works in FastAPI!
    """
    def decorator(func: Callable) -> Callable:
        # Register the route
        routes[path] = func
        print(f"✓ Registered route: {path} -> {func.__name__}")
        return func
    return decorator


# Define routes using the decorator
@route("/shipment")
def get_shipment() -> dict[str, str]:
    return {
        "content": "wooden table",
        "status": "in transit"
    }


@route("/users")
def get_users() -> list[str]:
    return ["Alice", "Bob", "Charlie"]


@route("/")
def home() -> str:
    return "Welcome to our API!"


# Simulate a simple server
print("\n" + "=" * 50)
print("Example 6: Simulating FastAPI Routing")
print("=" * 50)
print("\nRegistered routes:")
for path in routes:
    print(f"  - {path}")

# Simulate handling requests
def handle_request(request_path: str):
    """Simulate handling an HTTP request"""
    if request_path in routes:
        response = routes[request_path]()
        print(f"\n✓ Request: GET {request_path}")
        print(f"  Response: {response}")
    else:
        print(f"\n✗ Request: GET {request_path}")
        print("  Error: 404 Not Found")


print("\n--- Testing Requests ---")
handle_request("/shipment")
handle_request("/users")
handle_request("/")
handle_request("/docs")  # This will return 404

