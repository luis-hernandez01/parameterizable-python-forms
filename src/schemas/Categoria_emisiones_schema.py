from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CategoriaSchema(BaseModel):
    id: int
    nombre: str


class CategoriaCreate(BaseModel):
    nombre: str


class CategoriaUpdate(BaseModel):
    nombre: str


class CategoriaResponse(CategoriaSchema):
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
    items: List[CategoriaSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
