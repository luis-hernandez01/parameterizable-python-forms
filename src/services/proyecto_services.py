from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.Proyecto_model import (ProyectoAika, ProyectoWayra)
from src.models.logs_model import TipoOperacionEnum
from src.schemas.proyecto_schema import proyectoCreate, ProyectoUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import registrar_log, LogUtil
from sqlalchemy import asc

# Servicio para listar las unidades de ejecucion
class ProyectoService:
    def __init__(self, db: Session):
        self.db = db
        
    
    def all(self):
        return (
            self.db.query(ProyectoAika)
            .filter(ProyectoAika.activo == True)
            .order_by(asc(ProyectoAika.nombre_unidades))
            .all()
        )
    
        
# servicio para listar  los registros
    def list_proyecto(self, skip: int, limit: int, filtros: str | None = None,
                            activo: bool | None = None):
        query = self.db.query(ProyectoAika)
        if activo is not None:
            query = query.filter(ProyectoAika.activo == activo)
        
        if filtros:
            query = query.filter(ProyectoAika.id.ilike(f"%{filtros}%"))
        
        return ( query.order_by(asc(ProyectoAika.id))
                .offset(skip)
                .limit(limit)
                .all()
                )
        
    def count_proyecto(self, activo: bool | None = None, filtros: str | None = None):
        query = self.db.query(ProyectoAika)

        if activo is not None:
            query = query.filter(ProyectoAika.activo == activo)

        if filtros:
            query = query.filter(ProyectoAika.id.ilike(f"%{filtros}%"))

        return query.count()
    
    
    # servicio para crear un registro
    def create_proyecto(self, payload: proyectoCreate, 
                            request: Request, tokenpayload: dict):
        modelos = [ProyectoAika, ProyectoWayra]
        for modelo, db in zip(modelos, self.db):
            data = payload.model_dump()
            
            try:
                for key in [
                    "id_unidad_ejecutora",
                    "id_direccion_territorial",
                    "id_tipo_proyecto",
                    "id_ruta",
                    "id_tramo_sector",
                    "id_clasificacion",
                    "id_modo_transporte",
                    "id_tipoclasificacion_modo",
                    "catalogo",
                ]:
                    if data.get(key) == 0:
                        data[key] = None
                        
                data["activo"] = True
                data["id_persona"] = tokenpayload.get("sub")
                data["created_at"] = datetime.utcnow()
                entity = modelo(**data)
                
                db.add(entity)
                db.commit()
                db.refresh(entity)
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Error insertando en {modelo.__table__.schema}: {e}")
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="proyecto",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
    
    
    
    def show(self, proyecto_id: int):
        entity = self.db.query(ProyectoAika).filter(
            ProyectoAika.id == proyecto_id,
                ProyectoAika.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto no fue hallada")
        if proyecto_id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo proyecto_id se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    def update_proyecto(self, proyecto_id: int, 
                            payload: ProyectoUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db[0].query(ProyectoAika).filter(
            ProyectoAika.id == proyecto_id,
                ProyectoAika.activo == True).first()
        
        if not dataupdate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto no fue hallada")
        
            
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")
            
        modelos = [ProyectoAika, ProyectoAika]
        for modelo, db in zip(modelos, self.db):
            try:
                dataupdate = (
                    db.query(modelo)
                    .filter(modelo.id == proyecto_id, modelo.activo == True)
                    .first()
                )
                if dataupdate:
                    for field, value in payload.model_dump(exclude_unset=True).items():
                        # 🔍 Convierte automáticamente valores 0 en None para claves foráneas
                        if field in [
                            "id_unidad_ejecutora",
                            "id_direccion_territorial",
                            "id_tipo_proyecto",
                            "id_ruta",
                            "id_tramo_sector",
                            "id_clasificacion",
                            "id_modo_transporte",
                            "id_tipoclasificacion_modo",
                            "catalogo",
                        ] and value == 0:
                            value = None

                        setattr(dataupdate, field, value)

                    #  Campos de auditoría
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
            tabla_afectada="proyecto",
            id_registro_afectado=dataupdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataupdate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=dataupdate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(dataupdate)
    
    
    # servicio para eliminar logicamente un registro
    def delete_proyecto(self, proyecto_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db[0].query(ProyectoAika).filter(
            ProyectoAika.id == proyecto_id,
                ProyectoAika.activo == True).first()
        if not datadelete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto no fue hallada")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
        modelos = [ProyectoAika, ProyectoWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                datadelete = db.query(modelo).filter(modelo.id == proyecto_id, modelo.activo == True).first()
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
            tabla_afectada="proyecto",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datadelete)
    
    
    # servicio para reactivar logicamente un registro
    def reactivate(self, proyecto_id: int, request: Request, tokenpayload: dict):
        datareactivate = self.db[0].query(ProyectoAika).filter(
            ProyectoAika.id == proyecto_id).first()
        if not datareactivate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        if datareactivate.activo:
            return HTTPException(status_code=status.HTTP_200_OK, detail="El registro ya se encuentra activo")
        
        datos_viejos = LogEntityRead.from_orm(datareactivate).model_dump(mode="json")
        
        modelos = [ProyectoAika, ProyectoWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                
                datareactivate = db.query(modelo).filter(modelo.id == proyecto_id).first()
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
            tabla_afectada="proyectos",
            id_registro_afectado=datareactivate.id,
            tipo_operacion=TipoOperacionEnum.REACTIVATE,
            datos_nuevos=LogEntityRead.from_orm(datareactivate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datareactivate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datareactivate)