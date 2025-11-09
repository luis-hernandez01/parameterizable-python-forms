from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, Text
from src.config.config import Base


def crear_modelo_unidad_ejecutora(base):
    """
    Crea dinámicamente la tabla 'unidades_ejecutoras'
    para el schema asociado a la Base recibida.
    """
    class UnidadEjecutora(base):
        __tablename__ = "unidades_ejecutoras"
        __table_args__ = {"schema": base.metadata.schema}

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
            Text,
            nullable=True,
            comment="Descripción detallada de la unidad ejecutora",
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

        # Campos de auditoría
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

    # Cambiar dinámicamente el nombre de la clase según el schema
    UnidadEjecutora.__name__ = f"UnidadEjecutora_{base.metadata.schema}"
    return UnidadEjecutora


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
UnidadEjecutoraAika = crear_modelo_unidad_ejecutora(Base[0])
UnidadEjecutoraWayra = crear_modelo_unidad_ejecutora(Base[1])
