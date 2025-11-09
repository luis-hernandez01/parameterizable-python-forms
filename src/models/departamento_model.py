from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_departamento(base):
    """
    Crea dinámicamente la tabla 'departamentos'
    para el schema asociado a la Base recibida.
    """
    class Departamento(base):
        __tablename__ = "departamentos"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del departamento")
        nombre = Column(String(100), nullable=False, unique=True, comment="Nombre del departamento")
        codigo_dane = Column(String(5), nullable=True, comment="Código DANE del departamento")

        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, default=True, nullable=False, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambia dinámicamente el nombre de la clase según el schema
    Departamento.__name__ = f"Departamento_{base.metadata.schema}"
    return Departamento


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
DepartamentoAika = crear_modelo_departamento(Base[0])
DepartamentoWayra = crear_modelo_departamento(Base[1])
