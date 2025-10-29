from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class TrimestreSchema(BaseModel):
    id: int
    nombre: str

class TrimestreCreate(BaseModel):
    nombre: str

class TrimestreUpdate(BaseModel):
    nombre: str

class TrimestreResponse(TrimestreSchema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    nombre: str
    id_persona: int
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class TrimestreListResponse(BaseModel):
    data: List[TrimestreSchema]
    pagination: PaginacionSchema

