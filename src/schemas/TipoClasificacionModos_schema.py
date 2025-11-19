from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class TipoClasificacionModosSchema(BaseModel):
    id: int
    nombre: str
    activo: bool

class TipoClasificacionModosCreate(BaseModel):
    nombre: str

class TipoClasificacionModosUpdate(BaseModel):
    nombre: str

class TipoClasificacionModosResponse(TipoClasificacionModosSchema):
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
    items: List[TipoClasificacionModosSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int

