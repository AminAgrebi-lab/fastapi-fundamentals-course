from typing import Any

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(
    title="Module 2: Simple Database",
    description="Learning simple data storage with Python dictionaries",
    version="1.0.0"
)


# 📦 Simple Database (Python Dictionary)
shipments: dict[int, dict[str, Any]] = {
    12701: {
        "id": 12701,
        "weight": 0.6,
        "content": "glassware",
        "status": "placed"
    },
    12702: {
        "id": 12702,
        "weight": 2.3,
        "content": "books",
        "status": "shipped"
    },
    12703: {
        "id": 12703,
        "weight": 1.1,
        "content": "electronics",
        "status": "delivered"
    },
    12704: {
        "id": 12704,
        "weight": 3.5,
        "content": "furniture",
        "status": "in transit"
    },
    12705: {
        "id": 12705,
        "weight": 0.9,
        "content": "clothing",
        "status": "returned"
    },
    12706: {
        "id": 12706,
        "weight": 4.0,
        "content": "appliances",
        "status": "processing"
    },
    12707: {
        "id": 12707,
        "weight": 1.8,
        "content": "toys",
        "status": "placed"
    },
}


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "module": "Module 2: Simple Database",
        "message": "Using Python dictionary as a simple data store"
    }


# ✅ Static route FIRST
@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    """
    Get the latest shipment (highest ID)
    Uses max() on dictionary keys to find the most recent shipment
    """
    latest_id = max(shipments.keys())
    return {
        "message": "Latest shipment",
        "data": shipments[latest_id]
    }


# ✅ Dynamic route AFTER
@app.get("/shipment/{shipment_id}")
def get_shipment(shipment_id: int) -> dict[str, Any]:
    """
    Get a specific shipment by ID
    
    Args:
        shipment_id (int): The ID of the shipment to retrieve
    
    Returns:
        Shipment data if found, error message if not
    """
    # Error handling
    if shipment_id not in shipments:
        return {
            "detail": f"Shipment with ID {shipment_id} doesn't exist!"
        }
    
    return {
        "message": f"Shipment {shipment_id} found",
        "data": shipments[shipment_id]
    }


# 🎁 Bonus: Get all shipments
@app.get("/shipments")
def get_all_shipments() -> dict[str, Any]:
    """Get all shipments from the database"""
    return {
        "total": len(shipments),
        "shipments": list(shipments.values())
    }


# 📚 Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    """
    Custom Scalar API documentation endpoint
    Hidden from the main API schema
    """
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title + " - Scalar Docs",
    )