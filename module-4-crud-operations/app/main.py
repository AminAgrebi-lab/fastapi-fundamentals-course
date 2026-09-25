from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference


app = FastAPI(
    title="Module 4: CRUD Operations - PUT Method",
    description="Learning full updates with PUT method",
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
        "module": "Module 4: CRUD Operations",
        "message": "Learning PUT method for full updates!"
    }


# ============================================
# 📮 CREATE: POST - Create New Shipment
# ============================================

@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(data: dict[str, str | int | float]) -> dict[str, Any]:
    """Create a new shipment"""
    if "content" not in data or "weight" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both 'content' and 'weight' are required!"
        )
    
    content = data["content"]
    weight = data["weight"]
    
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kg."
        )
    
    if weight <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight must be greater than zero!"
        )
    
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "weight": weight,
        "content": content,
        "status": "placed"
    }
    
    return {
        "message": "Shipment created successfully",
        "id": new_id,
        "data": shipments[new_id]
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
        "data": shipments[latest_id]
    }


@app.get("/shipment/{shipment_id}")
def get_shipment(shipment_id: int) -> dict[str, Any]:
    """Get a specific shipment by ID"""
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    
    return shipments[shipment_id]


@app.get("/shipments")
def get_all_shipments() -> dict[str, Any]:
    """Get all shipments"""
    return {
        "total": len(shipments),
        "shipments": list(shipments.values())
    }


# ============================================
# 🔄 UPDATE: PUT - Full Update (Replace All Fields)
# ============================================

@app.put("/shipment/{shipment_id}")
def update_shipment_full(
    shipment_id: int,
    data: dict[str, str | int | float]
) -> dict[str, Any]:
    """
    Full update - Replace ALL fields of a shipment
    
    Request Body (JSON):
    {
        "content": "new content",
        "weight": 2.5,
        "status": "shipped"
    }
    
    Note: All fields must be provided (full replacement)
    """
    # Check if shipment exists
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    
    # Validation: Check required fields
    if "content" not in data or "weight" not in data or "status" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields (content, weight, status) are required for full update!"
        )
    
    # Validation: Check weight
    weight = data["weight"]
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kg."
        )
    
    if weight <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight must be greater than zero!"
        )
    
    # Replace the entire shipment data
    shipments[shipment_id] = {
        "weight": weight,
        "content": data["content"],
        "status": data["status"]
    }
    
    return {
        "message": f"Shipment {shipment_id} updated successfully (full update)",
        "data": shipments[shipment_id]
    }

# ============================================
# 🔄 UPDATE: PATCH - Partial Update (Update Specific Fields)
# ============================================

@app.patch("/shipment/{shipment_id}")
def update_shipment_partial(
    shipment_id: int,
    body: dict[str, Any]
) -> dict[str, Any]:
    """
    Partial update - Update ONLY the provided fields in the Request Body.
    
    Request Body (JSON):
    {
        "status": "delivered"
    }
    OR
    {
        "content": "new content",
        "weight": 2.5
    }
    """
    # 1. Check if shipment exists
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    
    # 2. Get the current shipment
    shipment = shipments[shipment_id]
    
    # 3. Update ONLY the fields provided in the body
    # The .update() method merges the new dictionary into the old one
    shipment.update(body)
    
    # 4. Save it back to the database
    shipments[shipment_id] = shipment
    
    return {
        "message": f"Shipment {shipment_id} updated successfully (partial update)",
        "updated_fields": list(body.keys()),
        "data": shipments[shipment_id]
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