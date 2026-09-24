from fastapi import FastAPI

app = FastAPI(
    title="Module 3: Query Parameters",
    description="Learning query parameters, HTTP exceptions, and POST requests",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "module": "Module 3: Query Parameters",
        "message": "Welcome! Let's learn about query parameters and more."
    }


# We'll add query parameters in the next lessons!