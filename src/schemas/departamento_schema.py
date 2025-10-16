from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class DepartamentoSchema(BaseModel):
    nombre: str
    codigo_dane: Optional[str]


class DepartamentoCreate(DepartamentoSchema):
    pass


class DepartamentoUpdate(DepartamentoSchema):
    pass


class DepartamentoResponse(DepartamentoSchema):
    id: int


class LogEntityRead(BaseModel):
    id: int
    nombre: str
    codigo_dane: Optional[str]
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


class DepartamentoListResponse(BaseModel):
    data: List[DepartamentoSchema]
    pagination: PaginacionSchema
