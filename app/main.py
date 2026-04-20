import logging
from fastapi import FastAPI
from app.core.db import lifespan
from app.api.upload import router as upload_router
from app.api.documentation import router as documentation_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Doc Assistant",
    description="LLM-Powered API Documentation Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(upload_router, prefix="/api/v1", tags=["Specifications"])
app.include_router(documentation_router, prefix="/api/v1/documentation", tags=["Documentation"])


@app.get("/")
def read_root():
    logger.info("Root endpoint was accessed")
    return {"message": "Welcome to API Doc Assistant!"}
