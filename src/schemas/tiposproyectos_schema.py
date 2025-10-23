from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class TiposproyectosSchema(BaseModel):
    id: int
    nombre: str
    requiere_licencia: bool

class TiposproyectosCreate(BaseModel):
    nombre: str
    requiere_licencia: bool

class TiposproyectosUpdate(BaseModel):
    nombre: str
    requiere_licencia: bool

class TiposproyectosResponse(TiposproyectosSchema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    nombre: str
    requiere_licencia: bool
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

class TiposproyectosListResponse(BaseModel):
    data: List[TiposproyectosSchema]
    pagination: PaginacionSchema

