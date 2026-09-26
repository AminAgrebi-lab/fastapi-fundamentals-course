from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

# استيراد النماذج الجديدة
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate

app = FastAPI(
    title="Module 5: Different Models",
    description="Using separate Pydantic models for different use cases",
    version="1.0.0",
)

# 📦 Simple Database
shipments: dict[int, dict[str, Any]] = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed", "destination": 11001, "client_email": "test@test.com"},
    12702: {"weight": 2.3, "content": "books", "status": "shipped", "destination": 11002, "client_email": "test@test.com"},
}


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to Module 5: Different Models"}

# ============================================
# 📮 CREATE: POST
# ============================================


@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "destination": shipment.destination,
        "client_email": shipment.client_email,
        "status": "placed",  # النظام يحدد الحالة تلقائياً
    }
    return {
        "message": "Shipment created successfully",
        "id": new_id,
        "data": shipments[new_id],
    }

# ============================================
# 📖 READ: GET (مع Response Model)
# ============================================


@app.get("/shipment/{shipment_id}", response_model=ShipmentRead)
def get_shipment(shipment_id: int):
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return shipments[shipment_id]

# ============================================
# 🔄 UPDATE: PATCH (مع Request & Response Models)
# ============================================


@app.patch("/shipment/{shipment_id}", response_model=ShipmentRead)
def update_shipment(shipment_id: int, update_data: ShipmentUpdate):
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    # تحديث الحقل المسموح به فقط
    shipments[shipment_id]["status"] = update_data.status.value
    return shipments[shipment_id]

# ============================================
# 📚 Scalar API Documentation
# ============================================


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title + " - Scalar Docs",
    )
