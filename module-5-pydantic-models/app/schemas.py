from pydantic import BaseModel, Field
from enum import Enum
import random

class ShipmentStatus(str, Enum):
    PLACED = "placed"
    IN_TRANSIT = "in_transit"
    FOR_DELIVERY = "for_delivery"
    DELIVERED = "delivered"

class ShipmentCreate(BaseModel):
    content: str = Field(..., max_length=100, description="Description of the shipment content")
    weight: float = Field(..., ge=1.0, le=25.0, description="Weight in kg (1 to 25)")
    destination: int | None = Field(
        default_factory=lambda: random.randint(11000, 11999), 
        description="Destination zip code"
    )
    client_email: str = Field(..., description="Client's email address")

# ============================================
# 📦 NEW: Response Model
# ============================================
class ShipmentResponse(BaseModel):
    """
    Model for the API response.
    FastAPI will use this to validate and filter the returned data.
    """
    content: str
    weight: float
    destination: int | None
    client_email: str
    status: ShipmentStatus = Field(default=ShipmentStatus.PLACED, description="Current status")