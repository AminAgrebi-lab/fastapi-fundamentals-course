from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

# استيراد الـ Models الجديدة
from .schemas import ShipmentCreate, ShipmentResponse, ShipmentStatus

app = FastAPI(
    title="Module 5: Response Models",
    description="Validating and filtering API responses",
    version="1.0.0",
)

# 📦 Simple Database
shipments: dict[int, dict[str, Any]] = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed", "destination": 11001, "client_email": "test@test.com", "internal_note": "Fragile!"},
    12702: {"weight": 2.3, "content": "books", "status": "shipped", "destination": 11002, "client_email": "test@test.com", "internal_note": "Heavy box"},
}

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to Module 5: Response Models"}

# ============================================
# 📮 CREATE: POST
# ============================================
@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    if shipment.weight > 25:
        raise HTTPException(status_code=406, detail="Maximum weight limit is 25 kg.")
    
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "destination": shipment.destination,
        "client_email": shipment.client_email,
        "status": "placed",
        "internal_note": "New shipment" # حقل إضافي للتجربة
    }
    
    return {"message": "Shipment created successfully", "id": new_id, "data": shipments[new_id]}

# ============================================
# 📖 READ: GET - مع Response Model!
# ============================================
@app.get("/shipment/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(shipment_id: int):
    """
    Get a specific shipment.
    The response_model argument ensures:
    1. Data is validated against ShipmentResponse.
    2. Extra fields (like 'internal_note') are filtered out and NOT sent to the client.
    """
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found",
        )
    
    # نرجع القاموس كما هو، و FastAPI سيتولى الباقي!
    return shipments[shipment_id]

@app.get("/shipments", response_model=list[ShipmentResponse])
def get_all_shipments():
    """Get all shipments (returns a list of ShipmentResponse)"""
    return list(shipments.values())

# ============================================
# 📚 Scalar API Documentation
# ============================================
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title + " - Scalar Docs",
    )