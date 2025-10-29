from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class Catalogoschema(BaseModel):
    id: int
    nombre: str
    modos: Optional[str]
    tipoclasificacion: Optional[str]

class CatalogoCreate(BaseModel):
    nombre: str
    id_modo: int
    id_tipo_clasificacion_modos: int

class CatalogoUpdate(BaseModel):
    nombre: str
    id_modo: int
    id_tipo_clasificacion_modos: int

class CatalogoResponse(Catalogoschema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    nombre: str
    id_modo: int
    id_tipo_clasificacion_modos: int
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

class CatalogoListResponse(BaseModel):
    data: List[Catalogoschema]
    pagination: PaginacionSchema

