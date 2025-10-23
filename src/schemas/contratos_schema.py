from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional, Literal
from datetime import datetime, date
from decimal import Decimal
import enum


class TipoContratoEnum(str, enum.Enum):
    obra = "obra"
    interventoria = "interventoria"
    convenio = "convenio"

class ContratoSchema(BaseModel):
    id: int
    id_proyecto: Optional[int]
    numero_contrato: str
    tipo_contrato: TipoContratoEnum
    fecha_contrato: Optional[date]
    objeto_contrato: Optional[str]
    fecha_inicio: Optional[date]
    fecha_terminacion: Optional[date]
    valor_contrato: Optional[Decimal]
    recursos_sostenibilidad: Optional[Decimal]
    
    @field_validator("tipo_contrato", mode="before")
    def validar_tipo_contrato(cls, v):
        if not v or not str(v).strip():
            raise ValueError("El campo tipo contrato está vacío. Ingresa un dato válido.")
        v = str(v).lower()
        if v not in ["obra", "interventoria", "convenio"]:
            raise ValueError("El campo tipo contrato debe ser 'obra', 'interventoria' o 'convenio'.")
        return v

    
    


class ContratoCreate(BaseModel):
    id_proyecto: Optional[int]
    numero_contrato: str
    tipo_contrato: TipoContratoEnum
    fecha_contrato: Optional[date]
    objeto_contrato: Optional[str]
    fecha_inicio: Optional[date]
    fecha_terminacion: Optional[date]
    valor_contrato: Optional[Decimal]
    recursos_sostenibilidad: Optional[Decimal]

class ContratoUpdate(BaseModel):
    id_proyecto: Optional[int]
    numero_contrato: str
    tipo_contrato: TipoContratoEnum
    fecha_contrato: Optional[date]
    objeto_contrato: Optional[str]
    fecha_inicio: Optional[date]
    fecha_terminacion: Optional[date]
    valor_contrato: Optional[Decimal]
    recursos_sostenibilidad: Optional[Decimal]

class ContratoResponse(ContratoSchema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    id_proyecto: Optional[int]
    numero_contrato: str
    tipo_contrato: Literal["obra", "interventoria", "convenio"]
    fecha_contrato: Optional[date]
    objeto_contrato: Optional[str]
    fecha_inicio: Optional[date]
    fecha_terminacion: Optional[date]
    valor_contrato: Optional[Decimal]
    recursos_sostenibilidad: Optional[Decimal]
    
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

class ContratoListResponse(BaseModel):
    data: List[ContratoSchema]
    pagination: PaginacionSchema

