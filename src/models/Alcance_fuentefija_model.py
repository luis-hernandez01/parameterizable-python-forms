from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_Alcance_fuentefija(base):
    """
    Crea dinámicamente la tabla 'Alcance'
    para el schema asociado a la Base recibida.
    """
    class Alcance_fuentefija(base):
        __tablename__ = "alcance"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del registro")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre del registro")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    Alcance_fuentefija.__name__ = f"Alcance_fuentefija_{base.metadata.schema}"
    return Alcance_fuentefija


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Alcance_fuentefijaAika = crear_modelo_Alcance_fuentefija(Base[0])
Alcance_fuentefijaWayra = crear_modelo_Alcance_fuentefija(Base[1])
