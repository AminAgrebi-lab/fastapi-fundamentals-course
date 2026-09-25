from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference


app = FastAPI(
    title="Module 3: Path & Query Parameters",
    description="Learning to combine path and query parameters",
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
        "module": "Module 3: Path & Query Parameters",
        "message": "Learning how to combine path and query parameters!"
    }


# ============================================
# 🔍 GET: Get Shipment by Query Parameter
# ============================================

@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    """
    Get shipment by ID using Query Parameter
    
    Examples:
    - /shipment?id=12701 → Get shipment 12701
    - /shipment          → Get latest shipment (no ID provided)
    """
    # If no ID provided, get the latest shipment
    if not id:
        id = max(shipments.keys())
    
    # Check if ID exists
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {id} doesn't exist!"
        )
    
    return shipments[id]


# ============================================
# 🛤️ GET: Get Shipment by Path Parameter
# ============================================

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    """Get the latest shipment (highest ID)"""
    latest_id = max(shipments.keys())
    return {
        "message": "Latest shipment",
        "data": shipments[latest_id]
    }


@app.get("/shipment/{shipment_id}")
def get_shipment_by_path(shipment_id: int) -> dict[str, Any]:
    """Get shipment by ID using Path Parameter"""
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    
    return shipments[shipment_id]


# ============================================
# 🎯 NEW: Get Specific Field from Shipment (Path + Query Combined!)
# ============================================

@app.get("/shipment/field/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    """
    Get a specific field from a specific shipment
    
    This endpoint combines:
    - Path Parameter: `field` (e.g., 'content', 'status', 'weight')
    - Query Parameter: `id` (the shipment ID)
    
    Examples:
    - /shipment/field/content?id=12701 → {"content": "glassware"}
    - /shipment/field/status?id=12704  → {"status": "in transit"}
    - /shipment/field/weight?id=12702  → {"weight": 2.3}
    
    Note:
    - FastAPI automatically distinguishes between path and query parameters
    - `field` is in the URL path → Path Parameter
    - `id` is NOT in the URL path → Query Parameter (must use ?id=...)
    """
    # 1. Check if shipment exists
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {id} not found"
        )
    
    shipment = shipments[id]
    
    # 2. Check if field exists in the shipment
    if field not in shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Field '{field}' does not exist in this shipment. Available fields: {list(shipment.keys())}"
        )
    
    # 3. Return the field value in a dictionary (Best Practice)
    # Note: Returning just the value (e.g., "glassware") is NOT recommended
    # Always wrap in a dictionary for consistent API responses
    return {field: shipment[field]}


# ============================================
# 📮 POST: Create New Shipment
# ============================================

@app.post("/shipment")
def submit_shipment(content: str, weight: float) -> dict[str, Any]:
    """
    Create a new shipment
    
    Args:
        content (str): The content of the shipment
        weight (float): The weight in kilograms
    
    Returns:
        The ID and data of the newly created shipment
    """
    # Validation: Check weight limit
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kg. Our delivery partners don't accept heavier shipments."
        )
    
    # Validation: Check for negative or zero weight
    if weight <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight must be greater than zero!"
        )
    
    # Validation: Check for empty content
    if not content or not content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content cannot be empty!"
        )
    
    # Generate new ID (max ID + 1)
    new_id = max(shipments.keys()) + 1
    
    # Create new shipment entry
    new_shipment = {
        "weight": weight,
        "content": content,
        "status": "placed"  # New shipments start as "placed"
    }
    
    # Add to our database
    shipments[new_id] = new_shipment
    
    # Return the new ID and data (Now matches dict[str, Any])
    return {
        "message": "Shipment created successfully",
        "id": new_id,
        "data": new_shipment
    }


# ============================================
# 📋 GET: Get All Shipments (Bonus)
# ============================================

@app.get("/shipments")
def get_all_shipments() -> dict[str, Any]:
    """Get all shipments from the database"""
    return {
        "total": len(shipments),
        "shipments": list(shipments.values())
    }


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