from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CombustibleSchema(BaseModel):
    id: int
    nombre: str
    activo: bool


class CombustibleCreate(BaseModel):
    nombre: str


class CombustibleUpdate(BaseModel):
    nombre: str


class CombustibleResponse(CombustibleSchema):
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
    items: List[CombustibleSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
