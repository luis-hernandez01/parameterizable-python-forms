from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from src.config.config import Base

class TramoSectores(Base):
    __tablename__ = "tramos_sectores"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Identificador único del tramo o sector")
    id_ruta = Column(Integer, ForeignKey("rutas_viales.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Ruta a la que pertenece el tramo")
    nombre = Column(String(255), nullable=False, comment="Nombre del tramo o sector")
    kilometraje_inicial = Column(DECIMAL(10, 3), nullable=True, comment="Kilometraje inicial del tramo")
    kilometraje_final = Column(DECIMAL(10, 3), nullable=True, comment="Kilometraje final del tramo")
    
    id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    

    # Relaciones
    ruta = relationship("RutasViales", backref="tramos")

    
    # Campos de auditoria
    created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
    updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

