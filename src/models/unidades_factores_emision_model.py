from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_unidades_factores_emision(base):
    """
    Crea dinámicamente la tabla 'unidades de emisiones'
    para el schema asociado a la Base recibida.
    """
    class Unidades_factores_emision(base):
        __tablename__ = "unidades_factores_emision"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la profesión")
        nombre = Column(String(255), unique=True, nullable=False)

        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Unidades_factores_emision.__name__ = f"Unidades_factores_emision_{base.metadata.schema}"
    return Unidades_factores_emision


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Unidades_factores_emisionAika = crear_modelo_unidades_factores_emision(Base[0])
Unidades_factores_emisionWayra = crear_modelo_unidades_factores_emision(Base[1])


