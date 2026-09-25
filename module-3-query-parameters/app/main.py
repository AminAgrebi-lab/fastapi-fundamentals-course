from typing import Any
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference


app = FastAPI(
    title="Module 3: Query Parameters",
    description="Learning query parameters, filtering, and optional values",
    version="1.0.0"
)


# ============================================
# 📦 Simple Database (Python Dictionary)
# ============================================

shipments: dict[int, dict[str, Any]] = {
    12701: {
        "weight": 0.6,
        "content": "glassware",
        "status": "placed"
    },
    12702: {
        "weight": 2.3,
        "content": "books",
        "status": "shipped"
    },
    12703: {
        "weight": 1.1,
        "content": "electronics",
        "status": "delivered"
    },
    12704: {
        "weight": 3.5,
        "content": "furniture",
        "status": "in transit"
    },
    12705: {
        "weight": 0.9,
        "content": "clothing",
        "status": "returned"
    },
    12706: {
        "weight": 4.0,
        "content": "appliances",
        "status": "processing"
    },
    12707: {
        "weight": 1.8,
        "content": "toys",
        "status": "placed"
    },
}


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "module": "Module 3: Query Parameters",
        "message": "Learning query parameters with optional values!"
    }


# ============================================
# 🔍 Get Shipment by Query Parameter
# ============================================

@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    """
    Get shipment by ID using Query Parameter
    
    Examples:
    - /shipment?id=12701 → Get shipment 12701
    - /shipment          → Get latest shipment (no ID provided)
    
    The 'id' parameter is:
    - Optional (int | None)
    - Defaults to None if not provided
    - Auto-validated by FastAPI
    """
    # If no ID provided, get the latest shipment
    if not id:
        id = max(shipments.keys())
    
    # Check if ID exists
    if id not in shipments:
        return {"detail": "Given id doesn't exist!"}
    
    return shipments[id]


# ============================================
# 📚 Scalar API Documentation
# ============================================

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    """Custom Scalar API documentation"""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title + " - Scalar Docs",
    )