from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class ClasificacionProyectoSchema(BaseModel):
    id: int
    nombre: str

class ClasificacionProyectoCreate(BaseModel):
    nombre: str

class ClasificacionProyectoUpdate(BaseModel):
    nombre: str

class UnidadEjecutoraResponse(ClasificacionProyectoSchema):
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
    items: List[ClasificacionProyectoSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int

