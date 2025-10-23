from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# from src.models.unidad_ejecutora_model import UnidadEjecutora
from src.config.config import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_unidad_ejecutora = Column(Integer, ForeignKey("unidades_ejecutoras.id"), nullable=True)
    id_direccion_territorial = Column(Integer, ForeignKey("direcciones_territoriales.id"), nullable=True)
    id_tipo_proyecto = Column(Integer, ForeignKey("tipos_proyecto.id"), nullable=True)
    id_ruta = Column(Integer, ForeignKey("rutas_viales.id"), nullable=True)
    id_tramo_sector = Column(Integer, ForeignKey("tramos_sectores.id"), nullable=True)
    id_clasificacion = Column(Integer, ForeignKey("clasificaciones_proyecto.id"), nullable=True)
    id_modo_transporte = Column(Integer, ForeignKey("modo.id"), nullable=True)
    id_funcionalidad = Column(Integer, ForeignKey("funcionalidades_carreteras.id"), nullable=True)
    id_categorizacion = Column(Integer, ForeignKey("categorizaciones_carreteras.id"), nullable=True)
    objeto_proyecto = Column(Text, nullable=True)
    resolucion_licencia = Column(String(100), nullable=True)
    fecha_resolucion = Column(Date, nullable=True)
    es_convenio_interadministrativo = Column(Boolean, default=False)
    numero_convenio = Column(String(100), nullable=True)
    
    # relaciones 
    
    
    # nombre_unidades = relationship(UnidadEjecutora, backref="proyecto")
    nombre_unidades = relationship("UnidadEjecutora", backref="proyecto")

    direccionesTerritoriales = relationship("DireccionesTerritoriales", backref="proyecto")
    tiposproyecto = relationship("TiposProyecto", backref="proyecto")
    rutasviales = relationship("RutasViales", backref="proyecto")
    tramosectores = relationship("TramoSectores", backref="proyecto")
    clasificacionesproyecto = relationship("ClasificacionesProyecto", backref="proyecto")
    modo = relationship("Modo", backref="proyecto")
    funcionalidadescarreteras = relationship("FuncionalidadesCarreteras", backref="proyecto")
    categorizacionescarreteras = relationship("CategorizacionesCarreteras", backref="proyecto")
    
    id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    
    # Campos de auditoria
    created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
    updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")