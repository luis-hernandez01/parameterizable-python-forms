from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class categorizacionchema(BaseModel):
    nombre: str

class categorizacionCreate(categorizacionchema):
    pass

class categorizacionUpdate(categorizacionchema):
    pass

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

