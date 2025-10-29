from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.TipoClasificacionModos_model import TipoClasificacionModos
from src.models.catalogomodoXtipoclasificacion_model import catalogomodoXtipoclasificacion

from src.models.logs_model import TipoOperacionEnum
from src.schemas.TipoClasificacionModos_schema import (TipoClasificacionModosCreate,
                                                    TipoClasificacionModosUpdate, LogEntityRead)
from datetime import datetime
from src.utils.logs_util import registrar_log, LogUtil

# Servicio para listar las unidades de ejecucion
class TipoClasificacionModosService:
    def __init__(self, db: Session):
        self.db = db
        
    async def all(self, id_modo):
        return (
            self.db.query(TipoClasificacionModos)
            .join(catalogomodoXtipoclasificacion)
            .filter(catalogomodoXtipoclasificacion.id_modo == id_modo,
                    catalogomodoXtipoclasificacion.activo == True)
            .distinct()
            .all()
        )
        
# servicio para listar  los registros
    def list_tipo_clasificacion(self, skip: int, limit: int):
        return self.db.query(TipoClasificacionModos).filter(TipoClasificacionModos.activo == True).offset(skip).limit(limit).all()
    def count_tipo_clasificacion(self):
        return self.db.query(TipoClasificacionModos).filter(TipoClasificacionModos.activo == True).count()
    
    
    # servicio para crear un registro
    async def create_tipo_clasificacion(self, payload: TipoClasificacionModosCreate, 
                            request: Request, tokenpayload: dict):
        datacreate = self.db.query(TipoClasificacionModos).filter(
            TipoClasificacionModos.nombre == payload.nombre,
                TipoClasificacionModos.activo == True).first()
        
        if datacreate:
            return HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="El tipo de clasificacion ya existe")
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        
        entity = TipoClasificacionModos(nombre=payload.nombre, id_persona=tokenpayload.get("sub"), 
                                        activo=True, created_at=datetime.utcnow())
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="tipo_clasificacion",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
    
    
    
    async def show(self, tipo_clacificacion_id: int):
        entity = self.db.query(TipoClasificacionModos).filter(
            TipoClasificacionModos.id == tipo_clacificacion_id,
                TipoClasificacionModos.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La funcionalidad no fue hallada")
        if tipo_clacificacion_id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo tipo_clacificacion_id se encuentra vacia ingresa un dato valido")
        return entity
    
    
    
    # servicio para editar logicamente un registro
    async def update_tipo_clasificacion(self, tipo_clasificacion_id: int, 
                            payload: TipoClasificacionModosUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db.query(TipoClasificacionModos).filter(
            TipoClasificacionModos.id == tipo_clasificacion_id,
                TipoClasificacionModos.activo == True).first()
        if payload.nombre:
            existe = (
                self.db.query(TipoClasificacionModos)
                .filter(TipoClasificacionModos.nombre == payload.nombre, TipoClasificacionModos.id != tipo_clasificacion_id)
                .first()
            )
            if existe:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado por otro registro."
                )
        
        if not dataupdate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La registro no fue hallada")
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
            
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")

        if dataupdate:
            dataupdate.nombre = payload.nombre
            dataupdate.id_persona = tokenpayload.get("sub")
            dataupdate.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(dataupdate)
            
            # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="tipo_clacificacion",
            id_registro_afectado=dataupdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataupdate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=dataupdate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(dataupdate)
    
    
    # servicio para eliminar logicamente un registro
    async def delete_tipo_clasificacion(self, tipo_clasificacion_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db.query(TipoClasificacionModos).filter(
            TipoClasificacionModos.id == tipo_clasificacion_id,
                TipoClasificacionModos.activo == True).first()
        if not datadelete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallado")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
    # le paso un valor false para realizar un sofdelete para un eliminado logico
        datadelete.activo = False
        datadelete.deleted_at = datetime.utcnow()
        datadelete.id_persona = tokenpayload.get("sub")
        # guardar los cambios
        self.db.commit()
        self.db.refresh(datadelete)
        
        
        registrar_log(LogUtil(self.db),
            tabla_afectada="tipo_clasificacion",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datadelete)