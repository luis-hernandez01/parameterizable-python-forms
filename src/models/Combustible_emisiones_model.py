from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_combustibles_emisiones(base):
    """
    Crea dinámicamente la tabla 'combustibles de emisiones'
    para el schema asociado a la Base recibida.
    """
    class Combustibles_emisiones(base):
        __tablename__ = "combustibles_emisiones"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la profesión")
        nombre = Column(String(255), unique=True, nullable=False)

        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Combustibles_emisiones.__name__ = f"Combustibles_emisiones_{base.metadata.schema}"
    return Combustibles_emisiones


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Combustibles_emisionesAika = crear_modelo_combustibles_emisiones(Base[0])
Combustibles_emisionesWayra = crear_modelo_combustibles_emisiones(Base[1])


