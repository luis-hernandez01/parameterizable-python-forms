from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class funcionalidades_carreteraSchema(BaseModel):
    nombre: str

class funcionalidades_carreteraCreate(funcionalidades_carreteraSchema):
    pass

class funcionalidades_carreteraUpdate(funcionalidades_carreteraSchema):
    pass

class funcionalidades_carreteraResponse(funcionalidades_carreteraSchema):
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

class FuncionalidadesListResponse(BaseModel):
    data: List[funcionalidades_carreteraSchema]
    pagination: PaginacionSchema

