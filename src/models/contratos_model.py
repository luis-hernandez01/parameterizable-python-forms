from sqlalchemy import (Column, Integer, String, 
                        Date, Text, DECIMAL, TIMESTAMP, 
                        ForeignKey, Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.config.config import Base
import enum
from sqlalchemy import Enum as SQLEnum


class TipoContratoEnum(str, enum.Enum):
    obra = "obra"
    interventoria = "interventoria"
    convenio = "convenio"

class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_proyecto = Column(Integer, ForeignKey("proyectos.id"), nullable=True)
    numero_contrato = Column(String(100), nullable=False, index=True)
    
    tipo_contrato = Column(
        SQLEnum(
            TipoContratoEnum,
            name="tipo_contrato_enum",
        ),
        nullable=False, index=True
    )
    


    fecha_contrato = Column(Date, nullable=True)
    objeto_contrato = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_terminacion = Column(Date, nullable=True)
    valor_contrato = Column(DECIMAL(18, 2), nullable=True)
    recursos_sostenibilidad = Column(DECIMAL(18, 2), nullable=True)
    
    tipo_contrato = Column(
        SQLEnum(
            TipoContratoEnum,
            name="tipo_contrato_enum",  # ⚠️ el nombre del tipo ENUM en PostgreSQL
            create_type=False,  # 👈 importante, evitar error si ya existe
            native_enum=True,
        ),
        nullable=False,
        index=True,
    )
    
    
    id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    
    # Campos de auditoria
    created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
    updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Relaciones
    proyecto = relationship("Proyecto", backref="contratos")