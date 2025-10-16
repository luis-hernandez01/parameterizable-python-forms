from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class DireccionTerritorialSchema(BaseModel):
    nombre: str
    region: Optional[str]

class DireccionTerritorialCreate(DireccionTerritorialSchema):
    pass

class DireccionTerritorialUpdate(DireccionTerritorialSchema):
    pass

class DireccionTerritorialResponse(DireccionTerritorialSchema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    nombre: str
    region: Optional[str]
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

class DireccionTerritorialListResponse(BaseModel):
    data: List[DireccionTerritorialSchema]
    pagination: PaginacionSchema

