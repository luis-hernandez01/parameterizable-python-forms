from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class TipoOperacionEnum(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class LogBase(BaseModel):
    tabla_afectada: str = Field(
        ..., max_length=100, description="Nombre de la tabla afectada por la operación"
    )
    id_registro_afectado: Optional[int] = Field(
        None, description="ID del registro afectado"
    )
    tipo_operacion: TipoOperacionEnum = Field(
        ..., description="Tipo de operación realizada"
    )
    datos_viejos: Optional[Dict[str, Any]] = Field(
        None, description="Datos anteriores del registro"
    )
    datos_nuevos: Optional[Dict[str, Any]] = Field(
        None, description="Datos nuevos del registro"
    )
    timestamp_operacion: Optional[datetime] = Field(
        default_factory=datetime.utcnow, description="Fecha y hora de la operación"
    )
    id_persona_operacion: Optional[int] = Field(
        None, description="Persona que realizó la operación"
    )
    ip_origen: Optional[str] = Field(
        None,
        max_length=45,
        description="Dirección IP desde donde se realizó la operación",
    )
    user_agent: Optional[str] = Field(
        None, description="User agent del navegador o aplicación"
    )


class LogCreate(LogBase):
    pass


class LogUpdate(LogBase):
    pass


class LogrResponse(LogBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
