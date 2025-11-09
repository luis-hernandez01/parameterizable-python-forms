from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.config.config import Base  # ← tu lista de bases con schemas

def crear_modelo_catalogomodoXtipoclasificacion(base):
    """
    Crea dinámicamente la tabla catalogo_modoXtipo_clasificacion
    para el schema asociado a la Base recibida.
    """
    class CatalogoModoXTipoClasificacion(base):
        __tablename__ = "catalogo_modoXtipo_clasificacion"
        

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la unidad ejecutora")
        nombre = Column(String(255), nullable=False, comment="Nombre de la unidad ejecutora")
        id_modo = Column(Integer, ForeignKey("modo.id"), nullable=True, comment="ID del modo")
        id_tipo_clasificacion_modos = Column(Integer, ForeignKey("tipo_clasificacion_modos.id"), nullable=True, comment="ID del tipo de clasificación de modos")

        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

        modos = relationship("Modo", backref="catalogo")
        tipoclasificacion = relationship("TipoClasificacionModos", backref="catalogo")

    CatalogoModoXTipoClasificacion.__name__ = f"CatalogoModoXTipoClasificacion_{base.metadata.schema}"
    return CatalogoModoXTipoClasificacion



# Crear los modelos para cada schema definido en config.py
CatalogoModoXTipoClasificacionAika = crear_modelo_catalogomodoXtipoclasificacion(Base[0])
CatalogoModoXTipoClasificacionWayra = crear_modelo_catalogomodoXtipoclasificacion(Base[1])
