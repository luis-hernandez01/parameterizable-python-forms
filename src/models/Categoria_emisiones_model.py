from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_categoria_emisiones(base):
    """
    Crea dinámicamente la tabla 'categorias de emisiones'
    para el schema asociado a la Base recibida.
    """
    class Categoria_emisiones(base):
        __tablename__ = "categoria_emisiones"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la profesión")
        nombre = Column(String(255), unique=True, nullable=False)

        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Categoria_emisiones.__name__ = f"Categoria_emisiones_{base.metadata.schema}"
    return Categoria_emisiones


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Categoria_emisionesAika = crear_modelo_categoria_emisiones(Base[0])
Categoria_emisionesnWayra = crear_modelo_categoria_emisiones(Base[1])


