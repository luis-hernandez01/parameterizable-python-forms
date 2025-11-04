from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DepartamentoSchema(BaseModel):
    id: int
    codigo: str = Field(..., max_length=2, description="Código del departamento (2 dígitos)")
    nombre: str = Field(..., max_length=100, description="Nombre del departamento")


class DepartamentoCreate(BaseModel):
    codigo: str = Field(..., max_length=2, description="Código del departamento (2 dígitos)")
    nombre: str = Field(..., max_length=100, description="Nombre del departamento")


class DepartamentoUpdate(BaseModel):
    codigo: str = Field(..., max_length=2, description="Código del departamento (2 dígitos)")
    nombre: str = Field(..., max_length=100, description="Nombre del departamento")


class DepartamentoResponse(DepartamentoSchema):
    id: int


class LogEntityRead(BaseModel):
    id: int
    codigo: str = Field(..., max_length=2, description="Código del departamento (2 dígitos)")
    nombre: str = Field(..., max_length=100, description="Nombre del departamento")
    id_persona: int
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginacionSchema(BaseModel):
    items: List[DepartamentoSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int


