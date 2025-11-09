from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_modo(base):
    """
    Crea dinámicamente la tabla 'modo'
    para el schema asociado a la Base recibida.
    """
    class Modo(base):
        __tablename__ = "modo"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del modo")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre del modo")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar la clase según el schema
    Modo.__name__ = f"Modo_{base.metadata.schema}"
    return Modo


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
ModoAika = crear_modelo_modo(Base[0])
ModoWayra = crear_modelo_modo(Base[1])
