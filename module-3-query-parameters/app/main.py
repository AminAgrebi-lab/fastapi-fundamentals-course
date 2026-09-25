from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference


app = FastAPI(
    title="Module 3: HTTP Exceptions",
    description="Learning proper error handling with HTTP exceptions",
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
        "module": "Module 3: HTTP Exceptions",
        "message": "Learning proper error handling!"
    }


# ============================================
# 🔍 Get Shipment by Query Parameter (WITH HTTP EXCEPTION)
# ============================================

@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    """
    Get shipment by ID using Query Parameter
    
    Examples:
    - /shipment?id=12701 → Get shipment 12701
    - /shipment          → Get latest shipment (no ID provided)
    
    Now with proper HTTP exceptions!
    """
    # If no ID provided, get the latest shipment
    if not id:
        id = max(shipments.keys())
    
    # Check if ID exists - RAISE HTTP EXCEPTION if not
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {id} doesn't exist!"
        )
    
    return shipments[id]


# ============================================
# 🛤️ Get Shipment by Path Parameter (WITH HTTP EXCEPTION)
# ============================================

@app.get("/shipment/{shipment_id}")
def get_shipment_by_path(shipment_id: int) -> dict[str, Any]:
    """
    Get shipment by ID using Path Parameter
    
    Example: /shipment/12701
    
    With proper HTTP exception handling!
    """
    # Check if ID exists
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    
    return shipments[shipment_id]


# ============================================
# 📊 Get Latest Shipment
# ============================================

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    """
    Get the latest shipment (highest ID)
    """
    latest_id = max(shipments.keys())
    return {
        "message": "Latest shipment",
        "data": shipments[latest_id]
    }


# ============================================
# 🎯 Example: Bad Request (400)
# ============================================

@app.get("/validate-weight/{weight}")
def validate_weight(weight: float) -> dict[str, Any]:
    """
    Validate shipment weight
    Returns 400 Bad Request if weight is negative
    """
    if weight < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight cannot be negative!"
        )
    
    return {
        "weight": weight,
        "valid": True,
        "message": "Weight is valid"
    }


# ============================================
# 🔐 Example: Unauthorized (401)
# ============================================

@app.get("/admin/shipments")
def get_admin_shipments(api_key: str | None = None) -> dict[str, Any]:
    """
    Admin endpoint - requires API key
    Returns 401 Unauthorized if no API key provided
    """
    # Simulate API key validation
    VALID_API_KEY = "secret-admin-key-123"
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required!",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    if api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key!"
        )
    
    return {
        "message": "Welcome, Admin!",
        "total_shipments": len(shipments),
        "all_shipments": list(shipments.values())
    }


# ============================================
# 🚫 Example: Forbidden (403)
# ============================================

@app.get("/users/{user_id}/delete")
def delete_user(user_id: int, role: str = "viewer") -> dict[str, str]:
    """
    Delete user - requires admin role
    Returns 403 Forbidden if user is not admin
    """
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete users!"
        )
    
    return {
        "message": f"User {user_id} deleted successfully"
    }


# ============================================
# 💥 Example: Internal Server Error (500)
# ============================================

@app.get("/process/{data}")
def process_data(data: str) -> dict[str, Any]:
    """
    Process data - simulates internal error
    Returns 500 Internal Server Error for specific cases
    """
    try:
        # Simulate processing
        if data == "error":
            raise ValueError("Simulated internal error!")
        
        return {
            "processed": data,
            "status": "success"
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal processing error: {str(e)}"
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