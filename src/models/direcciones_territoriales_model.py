from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_direcciones_territoriales(base):
    """
    Crea dinámicamente la tabla 'direcciones_territoriales'
    para el schema asociado a la Base recibida.
    """
    class DireccionesTerritoriales(base):
        __tablename__ = "direcciones_territoriales"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la dirección territorial")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre de la dirección territorial")
        descripcion = Column(Text, nullable=True, comment="Descripción o información adicional de la dirección territorial")

        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    DireccionesTerritoriales.__name__ = f"DireccionesTerritoriales_{base.metadata.schema}"
    return DireccionesTerritoriales


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
DireccionesTerritorialesAika = crear_modelo_direcciones_territoriales(Base[0])
DireccionesTerritorialesWayra = crear_modelo_direcciones_territoriales(Base[1])
