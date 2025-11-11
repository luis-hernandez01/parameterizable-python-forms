from datetime import datetime

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from src.models.logs_model import TipoOperacionEnum
from src.models.Combustible_emisiones_model import (Combustibles_emisionesAika, Combustibles_emisionesWayra)
from src.schemas.Combustibles_emisiones_schema import LogEntityRead, CombustibleCreate, CombustibleUpdate
from src.utils.logs_util import LogUtil, registrar_log


# Servicio para listar las unidades de ejecucion
class CombustibleService:
    def __init__(self, db: Session):
        self.db = db
    
    
    async def all(self):
        return (
            self.db.query(Combustibles_emisionesAika)
            .filter(Combustibles_emisionesAika.activo == True)
            .all()
        )
        

    # servicio para listar  los registros
    def lista(self, skip: int, limit: int, activo: bool | None = None):
        return (
            self.db.query(Combustibles_emisionesAika)
            .filter(Combustibles_emisionesAika.activo == activo)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self, activo: bool | None = None):
        return (
            self.db.query(Combustibles_emisionesAika)
            .filter(Combustibles_emisionesAika.activo == activo)
            .count()
        )

#     # servicio para crear un registro
    async def create(
        self, payload: CombustibleCreate, request: Request, tokenpayload: dict
    ):
        unidadcreate = (
            self.db[0].query(Combustibles_emisionesAika)
            .filter(
                Combustibles_emisionesAika.nombre == payload.nombre, Combustibles_emisionesAika.activo == True
            )
            .first()
        )
        if unidadcreate:
            return HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="La unidad ejecutora ya existe",
            )
        if payload.nombre == "":
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo nombre de la unidad ejecutora se encuentra vacia ingresa un dato valido",
            )
        if len(payload.nombre) > 255:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo nombre no puede tener un rango mayor a 255 caracteres",
            )
        
        modelos = [Combustibles_emisionesAika, Combustibles_emisionesWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                entity = modelo(
                    nombre=payload.nombre,
                    id_persona=tokenpayload.get("sub"),
                    activo=True,
                    created_at=datetime.utcnow(),
                )
                db.add(entity)
                db.commit()
                db.refresh(entity)
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando en {modelo.__table__.schema}: {e}")
        registrar_log(
            LogUtil(self.db),
            tabla_afectada="combustibles_emisiones",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1,
        )
        return LogEntityRead.from_orm(entity)

        

    async def show(self, combustible_id: int):
        entity = (
            self.db.query(Combustibles_emisionesAika)
            .filter(Combustibles_emisionesAika.id == combustible_id, Combustibles_emisionesAika.activo == True)
            .first()
        )
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El registro no fue hallada",
            )
        if combustible_id == "":
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo combustible_id se encuentra vacia ingresa un dato valido",
            )
        return entity

#     # servicio para editar logicamente un registro
    async def update(
        self,
        combustible_id: int,
        payload: CombustibleUpdate,
        request: Request,
        tokenpayload: dict,
    ):
        dataupdate = (
            self.db[0].query(Combustibles_emisionesAika)
            .filter(Combustibles_emisionesAika.id == combustible_id, Combustibles_emisionesAika.activo == True)
            .first()
        )
        if payload.nombre:
            existe = (
                self.db[0].query(Combustibles_emisionesAika)
                .filter(
                    Combustibles_emisionesAika.nombre == payload.nombre,
                    Combustibles_emisionesAika.id != combustible_id,
                )
                .first()
            )
            if existe:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado por otro registro.",
                )

        if not dataupdate:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El registro no fue hallada",
            )
        if payload.nombre == "":
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo nombre se encuentra vacia ingresa un dato valido",
            )
        if len(payload.nombre) > 255:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo nombre no puede tener un rango mayor a 255 caracteres",
            )
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")
            
        modelos = [Combustibles_emisionesAika, Combustibles_emisionesWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                dataupdate = (
                    db.query(modelo)
                    .filter(modelo.id == combustible_id, modelo.activo == True)
                    .first()
                )
                
                if dataupdate:
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
        registrar_log(
            LogUtil(self.db),
            tabla_afectada="combustibles_emisiones",
            id_registro_afectado=dataupdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataupdate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=dataupdate.id_persona,
            ip_origen=request.client.host,
            user_agent=1,
        )

        return LogEntityRead.from_orm(dataupdate)
                
        

    # servicio para eliminar logicamente un registro
    async def delete(self, combustible_id: int, request: Request, tokenpayload: dict):
        datadelete = (
            self.db[0].query(Combustibles_emisionesAika)
            .filter(Combustibles_emisionesAika.id == combustible_id, Combustibles_emisionesAika.activo == True)
            .first()
        )
        if not datadelete:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El registro no fue hallada",
            )
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
        modelos = [Combustibles_emisionesAika, Combustibles_emisionesWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                registro = db.query(modelo).filter(modelo.id == combustible_id, modelo.activo == True).first()
                if not registro:
                    continue
                # le paso un valor false para realizar un sofdelete para un eliminado logico
                registro.activo = False
                registro.deleted_at = datetime.utcnow()
                registro.id_persona = tokenpayload.get("sub")
                # guardar los cambios
                db.commit()
                db.refresh(registro)

                
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando en {modelo.__table__.schema}: {e}")
                
        
        registrar_log(
                    LogUtil(self.db),
                    tabla_afectada="combustibles_emisiones",
                    id_registro_afectado=registro.id,
                    tipo_operacion=TipoOperacionEnum.DELETE.value,
                    datos_nuevos=LogEntityRead.from_orm(registro).model_dump(mode="json"),
                    datos_viejos=datos_viejos,
                    id_persona_operacion=registro.id_persona,
                    ip_origen=request.client.host,
                    user_agent=1,
                )

        return LogEntityRead.from_orm(datadelete)


# servicio para reactivar logicamente un registro
    async def reactivate(self, combustible_id: int, request: Request, tokenpayload: dict):
        datareactivate = self.db[0].query(Combustibles_emisionesAika).filter(
            Combustibles_emisionesAika.id == combustible_id).first()
        if not datareactivate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        if datareactivate.activo:
            return HTTPException(status_code=status.HTTP_200_OK, detail="El registro ya se encuentra activo")
        datos_viejos = LogEntityRead.from_orm(datareactivate).model_dump(mode="json")
        
        modelos = [Combustibles_emisionesAika, Combustibles_emisionesWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                
                registro = db.query(modelo).filter(modelo.id == combustible_id).first()
                if not registro:
                    continue
            # le paso un valor false para realizar un sofdelete para un eliminado logico
                registro.activo = True
                registro.deleted_at = datetime.utcnow()
                registro.id_persona = tokenpayload.get("sub")
                # guardar los cambios
                db.commit()
                db.refresh(registro)
                
                
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando en {modelo.__table__.schema}: {e}")
        
        registrar_log(LogUtil(self.db),
                    tabla_afectada="combustibles_emisiones",
                    id_registro_afectado=registro.id,
                    tipo_operacion=TipoOperacionEnum.REACTIVATE,
                    datos_nuevos=LogEntityRead.from_orm(registro).model_dump(mode="json"),
                    datos_viejos=datos_viejos,
                    id_persona_operacion=registro.id_persona,
                    ip_origen=request.client.host,
                    user_agent=1)
        return LogEntityRead.from_orm(registro)