from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any


class EndpointAnalysisResponse(BaseModel):
    summary: Optional[str] = None
    request_docs: Optional[str] = None
    response_docs: Optional[str] = None
    example_payload: Optional[Union[Dict[str, Any], List[Any]]] = None
    validation_rules: Optional[str] = None
    missing_fields: Optional[List[str]] = None
