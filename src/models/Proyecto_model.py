from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from src.config.config import Base


def crear_modelo_proyecto(base):
    """
    Crea dinámicamente la tabla 'proyectos'
    para el schema asociado a la Base recibida.
    """
    class Proyecto(base):
        __tablename__ = "proyectos"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del proyecto")

        id_unidad_ejecutora = Column(Integer, ForeignKey("unidades_ejecutoras.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Unidad ejecutora asociada al proyecto")
        id_direccion_territorial = Column(Integer, ForeignKey("direcciones_territoriales.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Dirección territorial asociada al proyecto")
        id_tipo_proyecto = Column(Integer, ForeignKey("tipos_proyecto.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Tipo de proyecto")
        id_ruta = Column(Integer, ForeignKey("rutas_viales.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Ruta vial asociada")
        id_tramo_sector = Column(Integer, ForeignKey("tramos_sectores.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Tramo o sector asociado")
        id_clasificacion = Column(Integer, ForeignKey("clasificaciones_proyecto.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Clasificación del proyecto")
        id_modo_transporte = Column(Integer, ForeignKey("modo.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Modo de transporte del proyecto")
        id_tipoclasificacion_modo = Column(Integer, ForeignKey("tipo_clasificacion_modos.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Tipo de clasificación del modo")
        catalogo = Column(Integer, ForeignKey("catalogo_modoXtipo_clasificacion.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Catálogo de modo por tipo de clasificación")

        objeto_proyecto = Column(Text, nullable=True, comment="Descripción u objeto del proyecto")
        resolucion_licencia = Column(String(100), nullable=True, comment="Número de resolución de licencia del proyecto")
        fecha_resolucion = Column(Date, nullable=True, comment="Fecha de la resolución de licencia")
        es_convenio_interadministrativo = Column(Boolean, default=False, comment="Indica si el proyecto es un convenio interadministrativo")
        numero_convenio = Column(String(100), nullable=True, comment="Número de convenio si aplica")

        # Relaciones
        nombre_unidades = relationship("UnidadEjecutora", backref="proyecto")
        direccionesTerritoriales = relationship("DireccionesTerritoriales", backref="proyecto")
        tiposproyecto = relationship("TiposProyecto", backref="proyecto")
        rutasviales = relationship("RutasViales", backref="proyecto")
        tramosectores = relationship("TramoSectores", backref="proyecto")
        clasificacionesproyecto = relationship("ClasificacionesProyecto", backref="proyecto")
        modo = relationship("Modo", backref="proyecto")
        tipoclasificacion_modo = relationship("TipoClasificacionModos", backref="proyecto")
        catalogos = relationship("CatalogoModoXTipoClasificacion", backref="proyecto")

        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Proyecto.__name__ = f"Proyecto_{base.metadata.schema}"
    return Proyecto


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
ProyectoAika = crear_modelo_proyecto(Base[0])
ProyectoWayra = crear_modelo_proyecto(Base[1])
