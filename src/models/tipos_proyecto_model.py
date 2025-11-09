from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_tipos_proyecto(base):
    """
    Crea dinámicamente la tabla 'tipos_proyecto'
    para el schema asociado a la Base recibida.
    """
    class TiposProyecto(base):
        __tablename__ = "tipos_proyecto"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del tipo de proyecto")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre del tipo de proyecto")
        requiere_licencia = Column(Boolean, nullable=False, default=False, comment="Indica si el tipo de proyecto requiere licencia")
        
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    TiposProyecto.__name__ = f"TiposProyecto_{base.metadata.schema}"
    return TiposProyecto


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
TiposProyectoAika = crear_modelo_tipos_proyecto(Base[0])
TiposProyectoWayra = crear_modelo_tipos_proyecto(Base[1])
