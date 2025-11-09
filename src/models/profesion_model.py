from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_profesion(base):
    """
    Crea dinámicamente la tabla 'profesiones'
    para el schema asociado a la Base recibida.
    """
    class Profesion(base):
        __tablename__ = "profesiones"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la profesión")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre de la profesión o carrera")
        area_conocimiento = Column(String(100), nullable=True, comment="Área de conocimiento de la profesión")

        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Profesion.__name__ = f"Profesion_{base.metadata.schema}"
    return Profesion


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
ProfesionAika = crear_modelo_profesion(Base[0])
ProfesionWayra = crear_modelo_profesion(Base[1])
