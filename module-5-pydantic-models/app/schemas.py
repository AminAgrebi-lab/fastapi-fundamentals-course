from pydantic import BaseModel, Field
from enum import Enum
import random

class ShipmentStatus(str, Enum):
    PLACED = "placed"
    IN_TRANSIT = "in_transit"
    FOR_DELIVERY = "for_delivery"
    DELIVERED = "delivered"

# ============================================
# 🏗️ Base Model
# ============================================
class BaseShipment(BaseModel):
    content: str = Field(..., max_length=100, description="Description of the shipment content")
    weight: float = Field(..., ge=1.0, le=25.0, description="Weight in kg (1 to 25)")
    destination: int | None = Field(
        default_factory=lambda: random.randint(11000, 11999), 
        description="Destination zip code"
    )
    client_email: str = Field(..., description="Client's email address")

# ============================================
# 📦 Nested Model (Trick #1)
# ============================================
class Order(BaseModel):
    """Nested model representing an order inside a shipment"""
    title: str
    description: str
    price: float

# ============================================
# 📖 Read Model
# ============================================
class ShipmentRead(BaseShipment):
    status: ShipmentStatus = Field(default=ShipmentStatus.PLACED, description="Current status")
    order: Order | None = Field(default=None, description="Order details if available")

# ============================================
# 📮 Create Model
# ============================================
class ShipmentCreate(BaseShipment):
    order: Order | None = Field(default=None, description="Order details")

# ============================================
# 🔄 Update Model (Trick #3 Preparation)
# ============================================
class ShipmentUpdate(BaseModel):
    """All fields are optional for partial updates"""
    content: str | None = Field(default=None, max_length=100)
    weight: float | None = Field(default=None, ge=1.0, le=25.0)
    destination: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)