import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, TIMESTAMP, Boolean, BigInteger, JSON
)
from sqlalchemy import Enum as SQLEnum
from src.config.config import Base


class TipoOperacionEnum(str, enum.Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    REACTIVATE = "REACTIVATE"


def crear_modelo_logs(base):
    """
    Crea dinámicamente la tabla 'logs'
    para el schema asociado a la Base recibida.
    """
    class Logs(base):
        __tablename__ = "logs"

        id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="Identificador único del log")
        tabla_afectada = Column(String(100), nullable=False, comment="Nombre de la tabla afectada por la operación")
        id_registro_afectado = Column(Integer, nullable=True, comment="ID del registro afectado")
        
        tipo_operacion = Column(SQLEnum(TipoOperacionEnum, name="tipooperacionenum", schema=base.metadata.schema), nullable=False, comment="Tipo de operación realizada")
        
        datos_viejos = Column(JSON, nullable=True, comment="Datos anteriores del registro (para UPDATE y DELETE)")
        datos_nuevos = Column(JSON, nullable=True, comment="Datos nuevos del registro (para INSERT y UPDATE)")
        timestamp_operacion = Column(TIMESTAMP, nullable=True, default=datetime.utcnow, comment="Fecha y hora de la operación")
        id_persona_operacion = Column(Integer, nullable=True, comment="Persona que realizó la operación")
        ip_origen = Column(String(45), nullable=True, comment="Dirección IP desde donde se realizó la operación")
        user_agent = Column(Text, nullable=True, comment="User agent del navegador o aplicación")

        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    Logs.__name__ = f"Logs_{base.metadata.schema}"
    return Logs


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
LogsAika = crear_modelo_logs(Base[0])
LogsWayra = crear_modelo_logs(Base[1])
