from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.catalogomodoXtipoclasificacion_model import catalogomodoXtipoclasificacion
from src.models.logs_model import TipoOperacionEnum
from src.schemas.catalogomodoXtipoclasificacion_schema import CatalogoCreate, CatalogoUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import registrar_log, LogUtil

# Servicio para listar las unidades de ejecucion
class catalogoService:
    def __init__(self, db: Session):
        self.db = db
        
    async def all(self, id_modo, id_tipo):
        return (
            self.db.query(catalogomodoXtipoclasificacion)
            .filter(catalogomodoXtipoclasificacion.activo == True,
                    catalogomodoXtipoclasificacion.id_modo == id_modo,
                    catalogomodoXtipoclasificacion.id_tipo_clasificacion_modos == id_tipo)
            .all()
        )
    
        
# servicio para listar  los registros
    # def list_catalogo(self, skip: int, limit: int):
    #     return self.db.query(catalogomodoXtipoclasificacion).filter(catalogomodoXtipoclasificacion.activo == True).offset(skip).limit(limit).all()
    
    def list_catalogo(self, skip: int, limit: int, activo: bool | None = None):
        data = (
            self.db.query(catalogomodoXtipoclasificacion)
            .join(catalogomodoXtipoclasificacion.modos)
            .join(catalogomodoXtipoclasificacion.tipoclasificacion)
            .filter(catalogomodoXtipoclasificacion.activo == activo)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            {
                "id": rw.id,
                "nombre": rw.nombre,
                "id_modo": rw.modos.id if rw.modos else None,
                "id_tipo_clasificacion_modos": rw.tipoclasificacion.id if rw.tipoclasificacion else None,
                "modos": rw.modos.nombre if rw.modos else None,
                "tipoclasificacion": rw.tipoclasificacion.nombre if rw.tipoclasificacion else None
            }
            for rw in data
        ]
    
    
    def count_catalogo(self, activo: bool | None = None):
        return (self.db.query(catalogomodoXtipoclasificacion)
    .filter(catalogomodoXtipoclasificacion.activo == activo).count())
    
    
    # servicio para crear un registro
    async def create_catalogo(self, payload: CatalogoCreate, 
                            request: Request, tokenpayload: dict):
        
        
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre se encuentra vacia ingresa un dato valido")
        
        if payload.id_modo =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo modo se encuentra vacia ingresa un dato valido")
        
        if payload.id_tipo_clasificacion_modos =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo tipo clasificacion se encuentra vacia ingresa un dato valido")
        
        if len(payload.nombre) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        
        entity = catalogomodoXtipoclasificacion(nombre=payload.nombre, id_modo=payload.id_modo,
                                                id_tipo_clasificacion_modos=payload.id_tipo_clasificacion_modos,
                                                id_persona=tokenpayload.get("sub"), 
                                        activo=True, created_at=datetime.utcnow())
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="catalogo_modoXtipo_clasificacion",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
    
    
    
    async def show(self, catalogo_id: int):
        entity = self.db.query(catalogomodoXtipoclasificacion).filter(
            catalogomodoXtipoclasificacion.id == catalogo_id,
                catalogomodoXtipoclasificacion.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        if catalogo_id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo catalogo_id se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    async def update_catalogo(self, catalogo_id: int, 
                            payload: CatalogoUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db.query(catalogomodoXtipoclasificacion).filter(
            catalogomodoXtipoclasificacion.id == catalogo_id,
                catalogomodoXtipoclasificacion.activo == True).first()
        
        if not dataupdate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre se encuentra vacia ingresa un dato valido")
        if payload.id_modo =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo modo se encuentra vacia ingresa un dato valido")
        
        if payload.id_tipo_clasificacion_modos =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo tipo clasificacion se encuentra vacia ingresa un dato valido")
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
            tabla_afectada="catalogo_modoXtipo_clasificacion",
            id_registro_afectado=dataupdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataupdate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=dataupdate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(dataupdate)
    
    
    # servicio para eliminar logicamente un registro
    async def delete_catalogo(self, catalogo_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db.query(catalogomodoXtipoclasificacion).filter(
            catalogomodoXtipoclasificacion.id == catalogo_id,
                catalogomodoXtipoclasificacion.activo == True).first()
        if not datadelete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
    # le paso un valor false para realizar un sofdelete para un eliminado logico
        datadelete.activo = False
        datadelete.deleted_at = datetime.utcnow()
        datadelete.id_persona = tokenpayload.get("sub")
        # guardar los cambios
        self.db.commit()
        self.db.refresh(datadelete)
        
        
        registrar_log(LogUtil(self.db),
            tabla_afectada="catalogo_modoXtipo_clasificacion",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datadelete)
    
    
     # servicio para reactivar logicamente un registro
    async def reactivate(self, catalogo_id: int, request: Request, tokenpayload: dict):
        datareactivate = self.db.query(catalogomodoXtipoclasificacion).filter(
            catalogomodoXtipoclasificacion.id == catalogo_id).first()
        if not datareactivate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        if datareactivate.activo:
            return HTTPException(status_code=status.HTTP_200_OK, detail="El registro ya se encuentra activo")
        
        datos_viejos = LogEntityRead.from_orm(datareactivate).model_dump(mode="json")
    # le paso un valor false para realizar un sofdelete para un eliminado logico
        datareactivate.activo = True
        datareactivate.deleted_at = datetime.utcnow()
        datareactivate.id_persona = tokenpayload.get("sub")
        # guardar los cambios
        self.db.commit()
        self.db.refresh(datareactivate)
        
        
        registrar_log(LogUtil(self.db),
            tabla_afectada="catalogo_modoXtipo_clasificacion",
            id_registro_afectado=datareactivate.id,
            tipo_operacion=TipoOperacionEnum.REACTIVATE,
            datos_nuevos=LogEntityRead.from_orm(datareactivate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datareactivate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datareactivate)
    
    