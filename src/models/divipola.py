"""
Modelos de base de datos para DIVIPOLA
"""
from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.config.config import Base


class Departamento(Base):
    """Modelo de Departamento"""
    __tablename__ = "departamentos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(2), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    # Relación con municipios
    municipios = relationship("Municipio", back_populates="departamento", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre
        }


class Municipio(Base):
    """Modelo de Municipio"""
    __tablename__ = "municipios"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo_departamento = Column(String(2), ForeignKey("departamentos.codigo", ondelete="CASCADE"), nullable=False, index=True)
    codigo_municipio = Column(String(5), unique=True, nullable=False, index=True)
    nombre_municipio = Column(String(100), nullable=False, index=True)
    tipo_municipio = Column(String(50), default="Municipio")
    latitud = Column(DECIMAL(10, 7), nullable=True)
    longitud = Column(DECIMAL(10, 7), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    
    
    # Relación con departamento
    departamento = relationship("Departamento", back_populates="municipios")
    
    # Índice compuesto para coordenadas
    __table_args__ = (
        Index('idx_coordenadas', 'latitud', 'longitud'),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "codigo_departamento": self.codigo_departamento,
            "codigo_municipio": self.codigo_municipio,
            "nombre_municipio": self.nombre_municipio,
            "tipo_municipio": self.tipo_municipio,
            "latitud": float(self.latitud) if self.latitud else None,
            "longitud": float(self.longitud) if self.longitud else None
        }

