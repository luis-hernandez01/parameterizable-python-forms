from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class categorizacionchema(BaseModel):
    id: int
    nombre: str

class categorizacionCreate(BaseModel):
    nombre: str

class categorizacionUpdate(BaseModel):
    nombre: str

class categorizacionResponse(categorizacionchema):
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
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class categorizacionListResponse(BaseModel):
    data: List[categorizacionchema]
    pagination: PaginacionSchema

