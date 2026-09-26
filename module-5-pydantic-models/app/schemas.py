from enum import Enum
import random

from pydantic import BaseModel, Field

class ShipmentStatus(str, Enum):
    PLACED = "placed"
    IN_TRANSIT = "in_transit"
    FOR_DELIVERY = "for_delivery"
    DELIVERED = "delivered"

# ============================================
# 🏗️ Base Model (الحقول المشتركة)
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
# 📖 Read Model (للاستجابة)
# ============================================
class ShipmentRead(BaseShipment):
    """Includes all base fields + status"""
    status: ShipmentStatus = Field(default=ShipmentStatus.PLACED, description="Current status")

# ============================================
# 📮 Create Model (لإنشاء شحنة جديدة)
# ============================================
class ShipmentCreate(BaseShipment):
    """Inherits all base fields. Status is auto-set by server."""
    pass

# ============================================
# 🔄 Update Model (للتحديث الجزئي)
# ============================================
class ShipmentUpdate(BaseModel):
    """Only allows updating the status"""
    status: ShipmentStatus = Field(..., description="New status for the shipment")