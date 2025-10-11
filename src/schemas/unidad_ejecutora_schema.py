from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class UnidadEjecutoraSchema(BaseModel):
    nombre: str
    descripcion: Optional[str]

class UnidadEjecutoraCreate(UnidadEjecutoraSchema):
    pass

class UnidadEjecutoraUpdate(UnidadEjecutoraSchema):
    pass

class UnidadEjecutoraResponse(UnidadEjecutoraSchema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
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

class UnidadEjecutoraListResponse(BaseModel):
    data: List[UnidadEjecutoraSchema]
    pagination: PaginacionSchema

