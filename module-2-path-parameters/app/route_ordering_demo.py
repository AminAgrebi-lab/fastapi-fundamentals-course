"""
Route Ordering in FastAPI - Learning Notes

Key Concept:
============
The order in which you define routes matters!
FastAPI checks routes in the order they are defined.

Rule of Thumb:
==============
1. Define STATIC routes FIRST (e.g., /users/me, /products/featured)
2. Define DYNAMIC routes AFTER (e.g., /users/{id}, /products/{id})

Why?
====
If you define /users/{id} first, it will catch /users/me as well!
Because "me" will be treated as an {id} parameter.

Examples:
=========

# ✅ CORRECT ORDER
@app.get("/users/me")           # Static - defined first
def get_current_user():
    return {"user": "current"}

@app.get("/users/{user_id}")    # Dynamic - defined after
def get_user(user_id: int):
    return {"user_id": user_id}

# ❌ WRONG ORDER
@app.get("/users/{user_id}")    # Dynamic - catches everything!
def get_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/me")           # Never reached!
def get_current_user():
    return {"user": "current"}

Best Practices:
===============
1. Group related routes together
2. Put specific/static routes before generic/dynamic ones
3. Use clear naming conventions
4. Test all routes after defining them

Common Patterns:
================
- /users/me before /users/{id}
- /products/featured before /products/{id}
- /orders/pending before /orders/{id}
- /shipment/latest before /shipment/{id}
"""

print(__doc__)