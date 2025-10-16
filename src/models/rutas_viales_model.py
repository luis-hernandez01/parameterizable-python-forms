from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base

class RutasViales(Base):
    __tablename__ = "rutas_viales"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la unidad ejecutora")
    nombre = Column(String(255), unique=True, nullable=False, comment="Nombre de la unidad ejecutora")
    codigo = Column(String(25), nullable=True, comment="Codigo de la ruta vial")
    id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    
    # Campos de auditoria
    created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
    updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

