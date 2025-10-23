from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime, date

class Pyoyectochema(BaseModel):
    id_unidad_ejecutora: Optional[int]
    id_direccion_territorial: Optional[int]
    id_tipo_proyecto: Optional[int]
    id_ruta: Optional[int]
    id_tramo_sector: Optional[int]
    id_clasificacion: Optional[int]
    id_modo_transporte: Optional[int]
    id_funcionalidad: Optional[int]
    id_categorizacion: Optional[int]
    objeto_proyecto: Optional[str]
    resolucion_licencia: Optional[str]
    fecha_resolucion: Optional[date]
    es_convenio_interadministrativo: Optional[bool] = False
    numero_convenio: Optional[str]

class proyectoCreate(Pyoyectochema):
    pass

class ProyectoUpdate(Pyoyectochema):
    pass

class ProyectoResponse(Pyoyectochema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    
    id_unidad_ejecutora: Optional[int]
    id_direccion_territorial: Optional[int]
    id_tipo_proyecto: Optional[int]
    id_ruta: Optional[int]
    id_tramo_sector: Optional[int]
    id_clasificacion: Optional[int]
    id_modo_transporte: Optional[int]
    id_funcionalidad: Optional[int]
    id_categorizacion: Optional[int]
    objeto_proyecto: Optional[str]
    resolucion_licencia: Optional[str]
    fecha_resolucion: Optional[date]
    es_convenio_interadministrativo: Optional[bool] = False
    numero_convenio: Optional[str]
    
    id_persona: int
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class ProyectoListResponse(BaseModel):
    data: List[Pyoyectochema]
    pagination: PaginacionSchema

