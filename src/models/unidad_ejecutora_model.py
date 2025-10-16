from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, Text

from src.config.config import Base


class UnidadEjecutora(Base):
    __tablename__ = "unidades_ejecutoras"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        comment="Identificador único de la unidad ejecutora",
    )
    nombre = Column(
        String(255),
        unique=True,
        nullable=False,
        comment="Nombre de la unidad ejecutora",
    )
    descripcion = Column(
        Text, nullable=True, comment="Descripción detallada de la unidad ejecutora"
    )
    id_persona = Column(
        Integer,
        nullable=True,
        comment="ID de la persona que creó o modificó el registro",
    )
    activo = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Indica si el registro está activo (true) o inactivo (false)",
    )

    # Campos de auditoria
    created_at = Column(
        TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro"
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        comment="Fecha y hora de última actualización del registro",
    )
    deleted_at = Column(
        TIMESTAMP,
        nullable=True,
        comment="Fecha y hora de eliminación lógica del registro (soft delete)",
    )
