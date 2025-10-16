from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.config.config import Base

class Municipio(Base):
    __tablename__ = "municipios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del municipio")
    id_departamento = Column(Integer, ForeignKey("departamentos.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Departamento al que pertenece el municipio")
    nombre = Column(String(100), nullable=False, unique=True, comment="Nombre del municipio")
    codigo_dane = Column(String(8), nullable=True, comment="Código DANE del municipio")
    
    activo = Column(Boolean, default=True, nullable=False, comment="Indica si el registro está activo (true) o inactivo (false)")
    id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
    
    departamento = relationship("Departamento", backref="municipios")
    
    # Campos de auditoria
    created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
    updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")