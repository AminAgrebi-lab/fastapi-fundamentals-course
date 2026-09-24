from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

# Create FastAPI application instance with metadata
app = FastAPI(
    title="Shipment API",
    description="A simple API to manage shipment data",
    version="1.0.0",
    docs_url=None,  # Disable default Swagger UI
    redoc_url=None,  # Disable default ReDoc
)


@app.get("/")
def read_root():
    """Root endpoint - Welcome message"""
    return {
        "message": "🚀 Welcome to Shipment API",
        "version": "1.0.0",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "scalar": "/scalar",
            "openapi_spec": "/openapi.json"
        }
    }


@app.get("/health", include_in_schema=False)
def health_check():
    """Health check endpoint - Hidden from documentation"""
    return {
        "status": "healthy",
        "framework": "FastAPI"
    }


@app.get("/shipment")
def get_shipment():
    """Get shipment details"""
    return {
        "id": 1,
        "content": "wooden table",
        "status": "in transit",
        "origin": "New York",
        "destination": "Los Angeles"
    }


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI endpoint"""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """ReDoc endpoint (using default FastAPI ReDoc)"""
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
    )


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    """Scalar documentation endpoint"""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title + " - Scalar Docs",
    )