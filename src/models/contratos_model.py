from sqlalchemy import (
    Column, Integer, String, Date, Text, DECIMAL, TIMESTAMP,
    ForeignKey, Boolean, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
import enum
from src.config.config import Base


# ==========================================================
# ENUM: Tipo de Contrato
# ==========================================================
class TipoContratoEnum(str, enum.Enum):
    obra = "obra"
    interventoria = "interventoria"
    convenio = "convenio"


# ==========================================================
# FUNCIÓN: Crear modelo dinámico Contrato
# ==========================================================
def crear_modelo_contrato(base):
    """
    Crea dinámicamente la tabla 'contratos' para el schema asociado a la Base recibida.
    """
    class Contrato(base):
        __tablename__ = "contratos"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        id_proyecto = Column(Integer, ForeignKey("proyectos.id"), nullable=True, comment="ID del proyecto asociado")
        numero_contrato = Column(String(100), nullable=False, index=True, comment="Número del contrato")

        tipo_contrato = Column(
            SQLEnum(
                TipoContratoEnum,
                name="tipo_contrato_enum",     # nombre del tipo ENUM en PostgreSQL
                create_type=False,             # evita recrear el tipo si ya existe
                native_enum=True,
                schema=base.metadata.schema
            ),
            nullable=False,
            index=True,
            comment="Tipo de contrato: obra, interventoría o convenio",
        )

        fecha_contrato = Column(Date, nullable=True, comment="Fecha de firma del contrato")
        objeto_contrato = Column(Text, nullable=True, comment="Objeto del contrato")
        fecha_inicio = Column(Date, nullable=True, comment="Fecha de inicio del contrato")
        fecha_terminacion = Column(Date, nullable=True, comment="Fecha de terminación del contrato")
        valor_contrato = Column(DECIMAL(18, 2), nullable=True, comment="Valor total del contrato")
        recursos_sostenibilidad = Column(DECIMAL(18, 2), nullable=True, comment="Recursos destinados a sostenibilidad")

        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

        # Relaciones
        proyecto = relationship("Proyecto", backref="contratos")

    Contrato.__name__ = f"Contrato_{base.metadata.schema}"
    return Contrato


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
ContratoAika = crear_modelo_contrato(Base[0])
ContratoWayra = crear_modelo_contrato(Base[1])
