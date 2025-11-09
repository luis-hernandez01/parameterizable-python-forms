"""
Modelos dinámicos de base de datos para DIVIPOLA (Departamentos y Municipios)
"""
from sqlalchemy import (
    Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, Index, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.config.config import Base


# ==========================================================
# FUNCIÓN: crear_modelo_departamento
# ==========================================================
def crear_modelo_departamento(base):
    class Departamento(base):
        """Modelo de Departamento"""
        __tablename__ = "departamentos"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        codigo = Column(String(2), unique=True, nullable=False, index=True, comment="Código DANE del departamento")
        nombre = Column(String(100), nullable=False, index=True, comment="Nombre del departamento")

        created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="Fecha y hora de creación")
        updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment="Fecha y hora de última actualización")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica")

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

    Departamento.__name__ = f"Departamento_{base.metadata.schema}"
    return Departamento


# ==========================================================
# FUNCIÓN: crear_modelo_municipio
# ==========================================================
def crear_modelo_municipio(base):
    class Municipio(base):
        """Modelo de Municipio"""
        __tablename__ = "municipios"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        codigo_departamento = Column(String(2), ForeignKey("departamentos.codigo", ondelete="CASCADE"), nullable=False, index=True, comment="Código del departamento asociado")
        codigo_municipio = Column(String(5), unique=True, nullable=False, index=True, comment="Código DANE del municipio")
        nombre_municipio = Column(String(100), nullable=False, index=True, comment="Nombre del municipio")
        tipo_municipio = Column(String(50), default="Municipio", comment="Tipo de entidad territorial (Municipio, Distrito, etc.)")
        latitud = Column(DECIMAL(10, 7), nullable=True, comment="Latitud geográfica del municipio")
        longitud = Column(DECIMAL(10, 7), nullable=True, comment="Longitud geográfica del municipio")

        created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="Fecha y hora de creación")
        updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment="Fecha y hora de última actualización")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica")

        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Relación con departamento
        departamento = relationship("Departamento", back_populates="municipios")

        # Índice compuesto para coordenadas
        __table_args__ = (
            Index("idx_coordenadas", "latitud", "longitud"),
        )

        def to_dict(self):
            return {
                "id": self.id,
                "codigo_departamento": self.codigo_departamento,
                "codigo_municipio": self.codigo_municipio,
                "nombre_municipio": self.nombre_municipio,
                "tipo_municipio": self.tipo_municipio,
                "latitud": float(self.latitud) if self.latitud else None,
                "longitud": float(self.longitud) if self.longitud else None,
            }

    Municipio.__name__ = f"Municipio_{base.metadata.schema}"
    return Municipio


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
DepartamentoAika = crear_modelo_departamento(Base[0])
DepartamentoWayra = crear_modelo_departamento(Base[1])

MunicipioAika = crear_modelo_municipio(Base[0])
MunicipioWayra = crear_modelo_municipio(Base[1])
