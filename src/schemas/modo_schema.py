from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class ModoSchema(BaseModel):
    id: int
    nombre: str

class ModoCreate(BaseModel):
    nombre: str

class ModoUpdate(BaseModel):
    nombre: str

class ModoResponse(ModoSchema):
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

class ModoListResponse(BaseModel):
    data: List[ModoSchema]
    pagination: PaginacionSchema

