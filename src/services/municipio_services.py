from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.divipola import (MunicipioAika, MunicipioWayra, DepartamentoAika)
from src.models.logs_model import TipoOperacionEnum
from src.schemas.municipio_schema import municipioCreate, MunicipioUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import registrar_log, LogUtil
from sqlalchemy import asc

# Servicio para listar las unidades de ejecucion
class MunicipioService:
    def __init__(self, db: Session):
        self.db = db
        
    def all(self, codigo_departamento):
        return (
            self.db.query(MunicipioAika)
            .join(DepartamentoAika)
            .filter(DepartamentoAika.codigo == codigo_departamento,
                DepartamentoAika.activo == True)
            .order_by(asc(DepartamentoAika.nombre))
            .all()
        )
        
# servicio para listar  los registros
    def list_municipio(self, skip: int, limit: int, filtros: str | None = None,
                            activo: bool | None = None):
        query = self.db.query(MunicipioAika)
        if activo is not None:
            query = query.filter(MunicipioAika.activo == activo)
        
        if filtros:
            query = query.filter(MunicipioAika.nombre_municipio.ilike(f"%{filtros}%"))
        
        return ( query.order_by(asc(MunicipioAika.nombre_municipio))
                .offset(skip)
                .limit(limit)
                .all()
                )
        
    
    # este codigo comentado es para mostrar el valor del campo nombre
    # de la tabla foranea
    # en el schema se debe de agregar el nombre de la relacion
    
    # def list_municipio(self, skip: int, limit: int):
    #     municipios = (
    #         self.db.query(Municipio)
    #         .join(Municipio.departamento)
    #         .filter(Municipio.activo == True)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )
    #     return [
    #         {
    #             "nombre": m.nombre,
    #             "id_departamento": m.departamento.id if m.departamento else None,
    #             "codigo_dane": m.codigo_dane,
    #             "departamento": m.departamento.nombre if m.departamento else None
    #         }
    #         for m in municipios
    #     ]
    
    def count_municipio(self, activo: bool | None = None, filtros: str | None = None):
        query = self.db.query(MunicipioAika)

        if activo is not None:
            query = query.filter(MunicipioAika.activo == activo)

        if filtros:
            query = query.filter(MunicipioAika.nombre_municipio.ilike(f"%{filtros}%"))

        return query.count()
    
    
    
    # servicio para crear un registro
    def create_municipio(self, payload: municipioCreate, 
                            request: Request, tokenpayload: dict):
        datacreate = self.db[0].query(MunicipioAika).filter(
            MunicipioAika.nombre_municipio == payload.nombre_municipio).first()
        if datacreate:
            return HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="Este registro ya se encuentra creado. Se requiere su reactivación.")
        if payload.nombre_municipio =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre de el Municipio se encuentra vacia ingresa un dato valido")
        if len(payload.nombre_municipio) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        modelos = [MunicipioAika, MunicipioWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                entity = modelo(nombre_municipio=payload.nombre_municipio, codigo_departamento=payload.codigo_departamento,
                                codigo_municipio=payload.codigo_municipio, 
                                tipo_municipio=payload.tipo_municipio,
                                latitud=payload.latitud, longitud=payload.longitud,
                                id_persona=tokenpayload.get("sub"), 
                                                activo=True, created_at=datetime.utcnow())
                db.add(entity)
                db.commit()
                db.refresh(entity)
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando en {modelo.__table__.schema}: {e}")
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="municipio",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
    
    
    
    def show(self, municipio_id: int):
        entity = self.db.query(MunicipioAika).filter(
            MunicipioAika.id == municipio_id,
                MunicipioAika.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El Municipio no fue hallada")
        if municipio_id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo municipio_id se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    def update_municipio(self, municipio_id: int, 
                            payload: MunicipioUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db[0].query(MunicipioAika).filter(
            MunicipioAika.id == municipio_id,
                MunicipioAika.activo == True).first()
        if payload.nombre_municipio:
            existe = (
                self.db[0].query(MunicipioAika)
                .filter(MunicipioAika.nombre_municipio == payload.nombre_municipio, MunicipioAika.id != municipio_id)
                .first()
            )
            if existe:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre '{payload.nombre_municipio}' ya está siendo usado por otro Municipio."
                )
        
        if not dataupdate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El Municipio no fue hallada")
        if payload.nombre_municipio =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre de el Municipio se encuentra vacia ingresa un dato valido")
        if len(payload.nombre_municipio) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
            
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")
            
        modelos = [MunicipioAika, MunicipioWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                dataupdate = (
                    db.query(modelo)
                    .filter(modelo.id == municipio_id, modelo.activo == True)
                    .first()
                )

                if dataupdate:
                    dataupdate.codigo_departamento = payload.codigo_departamento
                    dataupdate.codigo_municipio = payload.codigo_municipio
                    dataupdate.nombre_municipio = payload.nombre_municipio
                    dataupdate.tipo_municipio = payload.tipo_municipio
                    dataupdate.latitud = payload.latitud
                    dataupdate.longitud = payload.longitud
                    
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
            tabla_afectada="municipio",
            id_registro_afectado=dataupdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataupdate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=dataupdate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(dataupdate)
    
    
    # servicio para eliminar logicamente un registro
    def delete_municipio(self, municipio_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db[0].query(MunicipioAika).filter(
            MunicipioAika.id == municipio_id,
                MunicipioAika.activo == True).first()
        if not datadelete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El Municipio no fue hallada")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
        modelos = [MunicipioAika, MunicipioWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                datadelete = db.query(modelo).filter(modelo.id == municipio_id, modelo.activo == True).first()
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
            tabla_afectada="municipio",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datadelete)
    
    
    # servicio para reactivar logicamente un registro
    def reactivate(self, municipio_id: int, request: Request, tokenpayload: dict):
        datareactivate = self.db[0].query(MunicipioAika).filter(
            MunicipioAika.id == municipio_id).first()
        if not datareactivate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        if datareactivate.activo:
            return HTTPException(status_code=status.HTTP_200_OK, detail="El registro ya se encuentra activo")
        
        datos_viejos = LogEntityRead.from_orm(datareactivate).model_dump(mode="json")
        
        modelos = [MunicipioAika, MunicipioWayra]
        for modelo, db in zip(modelos, self.db):
            try:
                datareactivate = db.query(modelo).filter(modelo.id == municipio_id).first()
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
            tabla_afectada="municipios",
            id_registro_afectado=datareactivate.id,
            tipo_operacion=TipoOperacionEnum.REACTIVATE,
            datos_nuevos=LogEntityRead.from_orm(datareactivate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datareactivate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datareactivate)