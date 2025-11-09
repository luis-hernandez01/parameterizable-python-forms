from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_tipo_clasificacion_modos(base):
    """
    Crea dinámicamente la tabla 'tipo_clasificacion_modos'
    para el schema asociado a la Base recibida.
    """
    class TipoClasificacionModos(base):
        __tablename__ = "tipo_clasificacion_modos"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del tipo de clasificación de modo")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre del tipo de clasificación de modo")

        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    TipoClasificacionModos.__name__ = f"TipoClasificacionModos_{base.metadata.schema}"
    return TipoClasificacionModos


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
TipoClasificacionModosAika = crear_modelo_tipo_clasificacion_modos(Base[0])
TipoClasificacionModosWayra = crear_modelo_tipo_clasificacion_modos(Base[1])
