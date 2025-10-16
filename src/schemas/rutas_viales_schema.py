from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class RutasSchema(BaseModel):
    nombre: str
    codigo: Optional[str]

class RutasCreate(RutasSchema):
    pass

class RutasUpdate(RutasSchema):
    pass

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
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class RutasListResponse(BaseModel):
    data: List[RutasSchema]
    pagination: PaginacionSchema

