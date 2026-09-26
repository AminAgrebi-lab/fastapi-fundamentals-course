from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate

app = FastAPI(
    title="Module 5: Pydantic Tips & Tricks",
    description="Advanced Pydantic techniques",
    version="1.0.0",
)

# 📦 Simple Database
shipments: dict[int, dict[str, Any]] = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed", "destination": 11001, "client_email": "test@test.com"},
}


@app.get("/")
def read_root():
    return {"message": "Welcome to Pydantic Tips & Tricks"}

# ============================================
# 📮 CREATE: POST (With Nested Model)
# ============================================


@app.post("/shipment", status_code=status.HTTP_201_CREATED, response_model=ShipmentRead)
def create_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    new_id = max(shipments.keys()) + 1

    # Trick #2: Convert Pydantic model to dictionary and unpack it
    new_shipment_data = shipment.model_dump()
    new_shipment_data["status"] = "placed"  # Force initial status

    shipments[new_id] = new_shipment_data

    return {
        "message": "Shipment created successfully",
        "id": new_id,
        "data": shipments[new_id],
    }

# ============================================
# 🔄 PATCH: Partial Update (The Magic Trick!)
# ============================================


@app.patch("/shipment/{shipment_id}", response_model=ShipmentRead)
def update_shipment(shipment_id: int, body: ShipmentUpdate):
    if shipment_id not in shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    #  Trick #3: The Magic of exclude_none=True
    # body.model_dump() returns ALL fields (missing ones are None).
    # body.model_dump(exclude_none=True) returns ONLY the fields the client sent!

    update_data = body.model_dump(exclude_none=True)

    print(f"🔍 Full Model Dump: {body.model_dump()}")
    print(f"✨ Filtered Dump (exclude_none=True): {update_data}")

    # Update the database dictionary ONLY with the provided fields
    shipments[shipment_id].update(update_data)

    return shipments[shipment_id]

# ============================================
#  READ: GET
# ============================================


@app.get("/shipment/{shipment_id}", response_model=ShipmentRead)
def get_shipment(shipment_id: int):
    if shipment_id not in shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")
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
