from fastapi import FastAPI
from typing import Any

app = FastAPI(
    title="Module 2: Simple Database",
    description="Using Python dictionary as a simple data store",
    version="1.0.0"
)


# ============================================
# 📦 Simple Database (Python Dictionary)
# ============================================

# This is our "database" - a dictionary where:
# - Keys: shipment IDs (integers)
# - Values: shipment data (dictionaries)
shipments: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "content": "wooden table",
        "status": "in transit",
        "weight": 15.5
    },
    2: {
        "id": 2,
        "content": "glassware set",
        "status": "delivered",
        "weight": 8.2
    },
    3: {
        "id": 3,
        "content": "leather sofa",
        "status": "placed",
        "weight": 45.0
    },
    4: {
        "id": 4,
        "content": "electronics",
        "status": "in transit",
        "weight": 3.7
    },
    5: {
        "id": 5,
        "content": "books collection",
        "status": "delivered",
        "weight": 12.3
    },
    6: {
        "id": 6,
        "content": "kitchen appliances",
        "status": "processing",
        "weight": 22.8
    },
    7: {
        "id": 7,
        "content": "winter clothing",
        "status": "in transit",
        "weight": 5.4
    }
}


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "module": "Module 2: Simple Database",
        "message": "Using Python dictionary as a simple data store"
    }


# ============================================
# 📊 Get Latest Shipment
# ============================================

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    """
    Get the latest shipment (highest ID)
    Since IDs are auto-incremented, the max ID is the latest
    """
    # Find the maximum ID (latest shipment)
    latest_id = max(shipments.keys())
    
    # Get the shipment with that ID
    latest_shipment = shipments[latest_id]
    
    return {
        "message": "Latest shipment",
        "data": latest_shipment
    }


# ============================================
# 🔍 Get Shipment by ID
# ============================================

@app.get("/shipment/{shipment_id}")
def get_shipment(shipment_id: int) -> dict[str, Any]:
    """
    Get a specific shipment by ID
    
    Args:
        shipment_id (int): The ID of the shipment to retrieve
    
    Returns:
        Shipment data if found, error message if not
    """
    # Error handling: Check if ID exists
    if shipment_id not in shipments:
        return {
            "detail": f"Shipment with ID {shipment_id} does not exist"
        }
    
    # Get the shipment from our "database"
    shipment = shipments[shipment_id]
    
    return {
        "message": f"Shipment {shipment_id} found",
        "data": shipment
    }


# ============================================
# 📋 Get All Shipments (Bonus)
# ============================================

@app.get("/shipments")
def get_all_shipments() -> dict[str, Any]:
    """
    Get all shipments from our simple database
    """
    return {
        "total": len(shipments),
        "shipments": list(shipments.values())
    }