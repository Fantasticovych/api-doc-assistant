from pydantic import BaseModel
from datetime import datetime


class APISpecificationResponse(BaseModel):
    id: str
    title: str | None = None
    format: str
    created_at: datetime
