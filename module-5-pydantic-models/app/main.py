from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(
    title="Module 5: Pydantic Models",
    description="Learning data validation with Pydantic",
    version="1.0.0",
)


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


# ============================================
# 📦 Simple Database
# ============================================

shipments: dict[int, dict[str, Any]] = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed"},
    12702: {"weight": 2.3, "content": "books", "status": "shipped"},
    12703: {"weight": 1.1, "content": "electronics", "status": "delivered"},
    12704: {"weight": 3.5, "content": "furniture", "status": "in transit"},
    12705: {"weight": 0.9, "content": "clothing", "status": "returned"},
    12706: {"weight": 4.0, "content": "appliances", "status": "processing"},
    12707: {"weight": 1.8, "content": "toys", "status": "placed"},
}


# ============================================
# 📦 Pydantic Model (NEW!)
# ============================================

class ShipmentCreate(BaseModel):
    """
    Pydantic model for creating a new shipment.
    Automatically validates:
    - Field types (str, float, int)
    - Required fields (all fields are required by default)
    """

    content: str
    weight: float
    destination: int  # Zip code
    client_email: str


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "module": "Module 5: Pydantic Models",
        "message": "Learning automatic validation with Pydantic!",
    }


# ============================================
#  CREATE: POST - Using Pydantic Model
# ============================================

@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    """
    Create a new shipment using Pydantic model validation.

    Request Body (JSON):
    {
        "content": "gaming laptop",
        "weight": 3.5,
        "destination": 12345,
        "client_email": "ahmed@example.com"
    }

    Pydantic automatically validates:
    - content must be string
    - weight must be float
    - destination must be int
    - client_email must be string
    - All fields are required
    """
    # Validation: Check weight limit
    if shipment.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kg.",
        )

    if shipment.weight <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight must be greater than zero!",
        )

    # Generate new ID
    new_id = max(shipments.keys()) + 1

    # Create new shipment using model data
    shipments[new_id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "destination": shipment.destination,
        "client_email": shipment.client_email,
        "status": "placed",
    }

    return {
        "message": "Shipment created successfully",
        "id": new_id,
        "data": shipments[new_id],
    }


# ============================================
# 📖 READ: GET - Retrieve Shipments
# ============================================

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    """Get the latest shipment"""
    latest_id = max(shipments.keys())
    return {
        "message": "Latest shipment",
        "data": shipments[latest_id],
    }


@app.get("/shipment/{shipment_id}")
def get_shipment(shipment_id: int) -> dict[str, Any]:
    """Get a specific shipment by ID"""
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found",
        )

    return shipments[shipment_id]


@app.get("/shipments")
def get_all_shipments() -> dict[str, Any]:
    """Get all shipments"""
    return {
        "total": len(shipments),
        "shipments": list(shipments.values()),
    }
