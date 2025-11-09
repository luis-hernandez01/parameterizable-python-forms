from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base  # lista de bases (por schema)

def crear_modelo_clasificaciones_proyecto(base):
    """
    Crea dinámicamente la tabla 'clasificaciones_proyecto'
    para el schema asociado a la Base recibida.
    """
    class ClasificacionesProyecto(base):
        __tablename__ = "clasificaciones_proyecto"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la clasificación de proyecto")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre de la clasificación del proyecto")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica (soft delete)")

    ClasificacionesProyecto.__name__ = f"ClasificacionesProyecto_{base.metadata.schema}"
    return ClasificacionesProyecto


# Instanciación para cada schema definido en config.py
ClasificacionesProyectoAika = crear_modelo_clasificaciones_proyecto(Base[0])
ClasificacionesProyectoWayra = crear_modelo_clasificaciones_proyecto(Base[1])
