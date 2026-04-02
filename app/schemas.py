from pydantic import BaseModel
from typing import Optional

class IdentifierCreate(BaseModel):
    identifier_name: str
    description: Optional[str] = None
    identifier_type: Optional[str] = None

class IdentifierResponse(BaseModel):
    identifier_name: str
    description: Optional[str] = None
    identifier_type: Optional[str] = None

    class Config:
        from_attributes = True

class IdentifierUpdate(BaseModel):
    description: Optional[str] = None
    identifier_type: Optional[str] = None