from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class MunicipioSchema(BaseModel):
    id: int
    codigo_departamento: str = Field(..., max_length=2, description="Código del departamento asociado")
    codigo_municipio: str = Field(..., max_length=5, description="Código único del municipio")
    nombre_municipio: str = Field(..., max_length=100, description="Nombre del municipio")
    tipo_municipio: Optional[str] = Field(default="Municipio", max_length=50)
    latitud: Optional[float] = Field(default=None, description="Latitud del municipio")
    longitud: Optional[float] = Field(default=None, description="Longitud del municipio")
    # departamento: Optional[str]



class municipioCreate(BaseModel):
    codigo_departamento: str = Field(..., max_length=2, description="Código del departamento asociado")
    codigo_municipio: str = Field(..., max_length=5, description="Código único del municipio")
    nombre_municipio: str = Field(..., max_length=100, description="Nombre del municipio")
    tipo_municipio: Optional[str] = Field(default="Municipio", max_length=50)
    latitud: Optional[float] = Field(default=None, description="Latitud del municipio")
    longitud: Optional[float] = Field(default=None, description="Longitud del municipio")


class MunicipioUpdate(BaseModel):
    codigo_departamento: str = Field(..., max_length=2, description="Código del departamento asociado")
    codigo_municipio: str = Field(..., max_length=5, description="Código único del municipio")
    nombre_municipio: str = Field(..., max_length=100, description="Nombre del municipio")
    tipo_municipio: Optional[str] = Field(default="Municipio", max_length=50)
    latitud: Optional[float] = Field(default=None, description="Latitud del municipio")
    longitud: Optional[float] = Field(default=None, description="Longitud del municipio")


class MunicipioResponse(MunicipioSchema):
    id: int


class LogEntityRead(BaseModel):
    id: int
    codigo_departamento: str = Field(..., max_length=2, description="Código del departamento asociado")
    codigo_municipio: str = Field(..., max_length=5, description="Código único del municipio")
    nombre_municipio: str = Field(..., max_length=100, description="Nombre del municipio")
    tipo_municipio: Optional[str] = Field(default="Municipio", max_length=50)
    latitud: Optional[float] = Field(default=None, description="Latitud del municipio")
    longitud: Optional[float] = Field(default=None, description="Longitud del municipio")
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
