from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ProfesionSchema(BaseModel):
    id: int
    nombre: str
    area_conocimiento: Optional[str]


class ProfesionCreate(BaseModel):
    nombre: str
    area_conocimiento: Optional[str]


class ProfesionUpdate(BaseModel):
    nombre: str
    area_conocimiento: Optional[str]


class ProfesionResponse(ProfesionSchema):
    id: int


class LogEntityRead(BaseModel):
    id: int
    nombre: str
    area_conocimiento: Optional[str]
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


class ProfesionListResponse(BaseModel):
    data: List[ProfesionSchema]
    pagination: PaginacionSchema
