from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_Categoria_fuentefija(base):
    """
    Crea dinámicamente la tabla 'categoria'
    para el schema asociado a la Base recibida.
    """
    class Categoria_fuentefija(base):
        __tablename__ = "categoria_funtefija"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del registro")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre del registro")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    Categoria_fuentefija.__name__ = f"Categoria_fuentefija_{base.metadata.schema}"
    return Categoria_fuentefija


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Categoria_fuentefijaAika = crear_modelo_Categoria_fuentefija(Base[0])
Categoria_fuentefijaWayra = crear_modelo_Categoria_fuentefija(Base[1])
