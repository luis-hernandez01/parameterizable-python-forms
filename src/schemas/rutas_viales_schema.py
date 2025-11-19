from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class RutasSchema(BaseModel):
    id: int
    nombre: str
    codigo: Optional[str]
    activo: bool

class RutasCreate(BaseModel):
    codigo: Optional[str]
    nombre: str

class RutasUpdate(BaseModel):
    codigo: Optional[str]
    nombre: str

class RutasResponse(RutasSchema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    nombre: str
    codigo: Optional[str]
    id_persona: int
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    items: List[RutasSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int

