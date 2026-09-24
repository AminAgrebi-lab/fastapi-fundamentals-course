from typing import Any

from fastapi import FastAPI


app = FastAPI(
    title="Module 2: Route Ordering",
    description="Understanding route order importance in FastAPI",
    version="1.0.0"
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "module": "Module 2: Route Ordering",
        "message": "Understanding the importance of route order!"
    }


# ============================================
# ❌ WRONG ORDER (Commented out - Don't use this!)
# ============================================

# This is WRONG because /shipment/{id} will catch "latest" as an ID
# @app.get("/shipment/{id}")
# def get_shipment(id: int) -> dict[str, Any]:
#     return {
#         "id": id,
#         "content": "wooden table",
#         "status": "in transit"
#     }
#
# @app.get("/shipment/latest")  # This will NEVER be reached!
# def get_latest_shipment() -> dict[str, Any]:
#     return {
#         "id": 999,
#         "content": "glassware",
#         "status": "placed",
#         "weight": 0.6
#     }


# ============================================
# ✅ CORRECT ORDER (Use this!)
# ============================================

# 1. Define STATIC routes FIRST
@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    """
    Get the latest shipment
    This MUST be defined BEFORE /shipment/{id}
    """
    return {
        "id": 999,
        "content": "glassware",
        "status": "placed",
        "weight": 0.6,
        "message": "This is the latest shipment"
    }


# 2. Define DYNAMIC routes AFTER
@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    """
    Get shipment by ID
    This is defined AFTER /shipment/latest
    """
    return {
        "id": id,
        "content": "wooden table",
        "status": "in transit",
        "weight": 15.5,
        "message": f"Shipment with ID {id}"
    }


# ============================================
# More Examples of Route Ordering
# ============================================

# Example 1: Users
@app.get("/users/me")
def get_current_user() -> dict[str, str]:
    """Get current user (static route - defined first)"""
    return {
        "id": "me",
        "name": "Ahmed",
        "email": "ahmed@example.com",
        "role": "admin"
    }


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, Any]:
    """Get user by ID (dynamic route - defined after)"""
    return {
        "id": user_id,
        "name": "User",
        "email": f"user{user_id}@example.com"
    }


# Example 2: Products
@app.get("/products/featured")
def get_featured_products() -> dict[str, Any]:
    """Get featured products (static route)"""
    return {
        "type": "featured",
        "products": ["Laptop", "Phone", "Tablet"],
        "count": 3
    }


@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict[str, Any]:
    """Get product by ID (dynamic route)"""
    return {
        "id": product_id,
        "name": "Product",
        "price": 99.99
    }


# Example 3: Orders with multiple static routes
@app.get("/orders/pending")
def get_pending_orders() -> dict[str, Any]:
    """Get all pending orders (static route #1)"""
    return {
        "status": "pending",
        "count": 5,
        "orders": [101, 102, 103, 104, 105]
    }


@app.get("/orders/completed")
def get_completed_orders() -> dict[str, Any]:
    """Get all completed orders (static route #2)"""
    return {
        "status": "completed",
        "count": 10,
        "orders": [201, 202, 203]
    }


@app.get("/orders/{order_id}")
def get_order(order_id: int) -> dict[str, Any]:
    """Get specific order by ID (dynamic route - defined last)"""
    return {
        "id": order_id,
        "status": "processing",
        "total": 299.99
    }
