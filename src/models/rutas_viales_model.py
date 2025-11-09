from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_rutas_viales(base):
    """
    Crea dinámicamente la tabla 'rutas_viales'
    para el schema asociado a la Base recibida.
    """
    class RutasViales(base):
        __tablename__ = "rutas_viales"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la ruta vial")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre de la ruta vial")
        codigo = Column(String(25), nullable=True, comment="Código de la ruta vial")

        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    RutasViales.__name__ = f"RutasViales_{base.metadata.schema}"
    return RutasViales


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
RutasVialesAika = crear_modelo_rutas_viales(Base[0])
RutasVialesWayra = crear_modelo_rutas_viales(Base[1])
