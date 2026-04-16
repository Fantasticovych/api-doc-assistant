from fastapi import FastAPI
from app.core.db import lifespan
from app.api.upload import router as upload_router

app = FastAPI(
    title="API Doc Assistant",
    description="LLM-Powered API Documentation Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(upload_router, prefix="/api/v1", tags=["Specifications"])


@app.get("/")
def read_root():
    return {"message": "Welcome to API Doc Assistant!"}
