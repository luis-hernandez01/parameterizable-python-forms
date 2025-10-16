import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    BigInteger,
    Column,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import (
    Integer,
    String,
    Text,
)

from src.config.config import Base


class TipoOperacionEnum(str, enum.Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class Log(Base):
    __tablename__ = "logs"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único del log",
    )
    tabla_afectada = Column(
        String(100),
        nullable=False,
        comment="Nombre de la tabla afectada por la operación",
    )
    id_registro_afectado = Column(
        Integer, nullable=True, comment="ID del registro afectado"
    )
    tipo_operacion = Column(
        SQLEnum(TipoOperacionEnum),
        nullable=False,
        comment="Tipo de operación realizada",
    )
    datos_viejos = Column(
        JSON,
        nullable=True,
        comment="Datos anteriores del registro (para UPDATE y DELETE)",
    )
    datos_nuevos = Column(
        JSON, nullable=True, comment="Datos nuevos del registro (para INSERT y UPDATE)"
    )
    timestamp_operacion = Column(
        TIMESTAMP,
        nullable=True,
        default=datetime.utcnow,
        comment="Fecha y hora de la operación",
    )
    id_persona_operacion = Column(
        Integer, nullable=True, comment="Persona que realizó la operación"
    )
    ip_origen = Column(
        String(45),
        nullable=True,
        comment="Dirección IP desde donde se realizó la operación",
    )
    user_agent = Column(
        Text, nullable=True, comment="User agent del navegador o aplicación"
    )
