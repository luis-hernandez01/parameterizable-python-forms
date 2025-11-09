from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_trimestre(base):
    """
    Crea dinámicamente la tabla 'trimestre'
    para el schema asociado a la Base recibida.
    """
    class Trimestre(base):
        __tablename__ = "trimestre"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del trimestre")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre del trimestre")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Trimestre.__name__ = f"Trimestre_{base.metadata.schema}"
    return Trimestre


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
TrimestreAika = crear_modelo_trimestre(Base[0])
TrimestreWayra = crear_modelo_trimestre(Base[1])
