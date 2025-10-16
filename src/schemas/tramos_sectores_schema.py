from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class TramoSchema(BaseModel):
    id_ruta: Optional[int] = Field(None, description="Ruta a la que pertenece el tramo")
    nombre: str = Field(..., max_length=255, description="Nombre del tramo o sector")
    kilometraje_inicial: Optional[Decimal] = Field(None, description="Kilometraje inicial del tramo")
    kilometraje_final: Optional[Decimal] = Field(None, description="Kilometraje final del tramo")

class TramoCreate(TramoSchema):
    pass

class TramoUpdate(TramoSchema):
    pass

class TramoResponse(TramoSchema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    id_ruta: Optional[int] = Field(None, description="Ruta a la que pertenece el tramo")
    nombre: str = Field(..., max_length=255, description="Nombre del tramo o sector")
    kilometraje_inicial: Optional[Decimal] = Field(None, description="Kilometraje inicial del tramo")
    kilometraje_final: Optional[Decimal] = Field(None, description="Kilometraje final del tramo")
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

class TramoListResponse(BaseModel):
    data: List[TramoSchema]
    pagination: PaginacionSchema

