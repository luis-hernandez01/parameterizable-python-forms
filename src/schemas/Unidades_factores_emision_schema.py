from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class UnidadFactorSchema(BaseModel):
    id: int
    nombre: str
    activo: bool


class UnidadFactorCreate(BaseModel):
    nombre: str


class UnidadFactorUpdate(BaseModel):
    nombre: str


class UnidadFactorResponse(UnidadFactorSchema):
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
    items: List[UnidadFactorSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
