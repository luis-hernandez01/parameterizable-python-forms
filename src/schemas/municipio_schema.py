from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class MunicipioSchema(BaseModel):
    nombre: str
    id_departamento: int
    codigo_dane: Optional[str]
    # departamento: Optional[str]



class municipioCreate(MunicipioSchema):
    pass


class MunicipioUpdate(MunicipioSchema):
    pass


class MunicipioResponse(MunicipioSchema):
    id: int


class LogEntityRead(BaseModel):
    id: int
    nombre: str
    id_departamento: int
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


class municipioListResponse(BaseModel):
    data: List[MunicipioSchema]
    pagination: PaginacionSchema
