from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.tramos_sectores_model import (TramoSectoresAika, TramoSectoresWayra)
from src.models.logs_model import TipoOperacionEnum
from src.schemas.tramos_sectores_schema import TramoCreate, TramoUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import registrar_log, LogUtil

# Servicio para listar las unidades de ejecucion
class TramoService:
    def __init__(self, db: Session):
        self.db = db
        
    async def all(self, id_ruta):
        return (
            self.db.query(TramoSectoresAika)
            .filter(TramoSectoresAika.id_ruta == id_ruta,
                    TramoSectoresAika.activo == True)
            .all()
        )
        
# servicio para listar  los registros
    def list_tramo(self, skip: int, limit: int, activo: bool | None = None):
        return self.db.query(TramoSectoresAika).filter(TramoSectoresAika.activo == activo).offset(skip).limit(limit).all()
    def count_tramo(self, activo: bool | None = None):
        return self.db.query(TramoSectoresAika).filter(TramoSectoresAika.activo == activo).count()
    
    
    # servicio para crear un registro
    async def create_tramo(self, payload: TramoCreate, 
                            request: Request, tokenpayload: dict):
        datacreate = self.db[0].query(TramoSectoresAika).filter(
            TramoSectoresAika.nombre == payload.nombre,
                TramoSectoresAika.activo == True).first()
        if datacreate:
            return HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="El tramo ya existe")
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre de el tramo se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        modelos = [TramoSectoresAika, TramoSectoresWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                entity = modelo(**payload.model_dump())
                entity.id_persona=tokenpayload.get("sub")
                entity.activo=True
                entity.created_at=datetime.utcnow()
                db.add(entity)
                db.commit()
                db.refresh(entity)
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando en {modelo.__table__.schema}: {e}")
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="tramos_sectores",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
    
    
    
    async def show(self, tramo_id: int):
        entity = self.db.query(TramoSectoresAika).filter(
            TramoSectoresAika.id == tramo_id,
                TramoSectoresAika.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El modo no fue hallada")
        if tramo_id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo tramo_id se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    async def update_tramo(self, tramo_id: int, 
                            payload: TramoUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db[0].query(TramoSectoresAika).filter(
            TramoSectoresAika.id == tramo_id,
                TramoSectoresAika.activo == True).first()
        if payload.nombre:
            existe = (
                self.db[0].query(TramoSectoresAika)
                .filter(TramoSectoresAika.nombre == payload.nombre, TramoSectoresAika.id != tramo_id)
                .first()
            )
            if existe:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado por otro modo."
                )
        
        if not dataupdate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tramo no fue hallada")
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre de el tramo se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
            
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")
            
        modelos = [TramoSectoresAika, TramoSectoresWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                dataupdate = (
                    db.query(modelo)
                    .filter(modelo.id == tramo_id, modelo.activo == True)
                    .first()
                )

                if dataupdate:
                    dataupdate.id_ruta = payload.id_ruta
                    dataupdate.nombre = payload.nombre
                    dataupdate.kilometraje_inicial = payload.kilometraje_inicial
                    dataupdate.kilometraje_final = payload.kilometraje_final
                    dataupdate.nombre = payload.nombre
                    
                    dataupdate.id_persona = tokenpayload.get("sub")
                    dataupdate.updated_at = datetime.utcnow()
                    db.commit()
                    db.refresh(dataupdate)
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando en {modelo.__table__.schema}: {e}")
            
            # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="tramos_sectores",
            id_registro_afectado=dataupdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataupdate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=dataupdate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(dataupdate)
    
    
    # servicio para eliminar logicamente un registro
    async def delete_tramo(self, tramo_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db[0].query(TramoSectoresAika).filter(
            TramoSectoresAika.id == tramo_id,
                TramoSectoresAika.activo == True).first()
        if not datadelete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tramo no fue hallada")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
        modelos = [TramoSectoresAika, TramoSectoresWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                datadelete = db.query(modelo).filter(modelo.id == tramo_id, modelo.activo == True).first()
                if not datadelete:
                    continue
            # le paso un valor false para realizar un sofdelete para un eliminado logico
                datadelete.activo = False
                datadelete.deleted_at = datetime.utcnow()
                datadelete.id_persona = tokenpayload.get("sub")
                # guardar los cambios
                db.commit()
                db.refresh(datadelete)

                
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando en {modelo.__table__.schema}: {e}")
        
        
        registrar_log(LogUtil(self.db),
            tabla_afectada="tramos_sectores",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datadelete)
    
    
    
    
    # servicio para reactivar logicamente un registro
    async def reactivate(self, tramo_id: int, request: Request, tokenpayload: dict):
        datareactivate = self.db[0].query(TramoSectoresAika).filter(
            TramoSectoresAika.id == tramo_id).first()
        if not datareactivate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        if datareactivate.activo:
            return HTTPException(status_code=status.HTTP_200_OK, detail="El registro ya se encuentra activo")
        
        datos_viejos = LogEntityRead.from_orm(datareactivate).model_dump(mode="json")
        
        modelos = [TramoSectoresAika, TramoSectoresWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                datareactivate = db.query(modelo).filter(modelo.id == tramo_id).first()
                if not datareactivate:
                    continue
        
            # le paso un valor false para realizar un sofdelete para un eliminado logico
                datareactivate.activo = True
                datareactivate.deleted_at = datetime.utcnow()
                datareactivate.id_persona = tokenpayload.get("sub")
                # guardar los cambios
                db.commit()
                db.refresh(datareactivate)
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando en {modelo.__table__.schema}: {e}")
        
        
        registrar_log(LogUtil(self.db),
            tabla_afectada="tramos_sectores",
            id_registro_afectado=datareactivate.id,
            tipo_operacion=TipoOperacionEnum.REACTIVATE,
            datos_nuevos=LogEntityRead.from_orm(datareactivate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datareactivate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datareactivate)