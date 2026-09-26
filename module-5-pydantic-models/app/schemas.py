import pydantic


class ShipmentCreate(pydantic.BaseModel):
    """
    Pydantic model for creating a new shipment.
    Includes advanced validation and default values.
    """
    content: str = pydantic.Field(
        ..., 
        max_length=100, 
        description="Description of the shipment content (max 100 chars)"
    )
    
    weight: float = pydantic.Field(
        ..., 
        ge=1.0, 
        le=25.0, 
        description="Weight of the shipment in kg (between 1 and 25 kg)"
    )
    
    destination: int | None = pydantic.Field(
        default=None,
        description="Destination zip code. Auto-generated if not provided."
    )
    
    client_email: str = pydantic.Field(
        ..., 
        description="Client's email address"
    )