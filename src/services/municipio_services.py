from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.municipio_model import Municipio
from src.models.logs_model import TipoOperacionEnum
from src.schemas.municipio_schema import municipioCreate, MunicipioUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import registrar_log, LogUtil

# Servicio para listar las unidades de ejecucion
class MunicipioService:
    def __init__(self, db: Session):
        self.db = db
        
# servicio para listar  los registros
    def list_municipio(self, skip: int, limit: int):
        return self.db.query(Municipio).filter(Municipio.activo == True).offset(skip).limit(limit).all()
    
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
    
    def count_municipio(self):
        return self.db.query(Municipio).filter(Municipio.activo == True).count()
    
    
    
    # servicio para crear un registro
    async def create_municipio(self, payload: municipioCreate, 
                            request: Request, tokenpayload: dict):
        datacreate = self.db.query(Municipio).filter(
            Municipio.nombre == payload.nombre,
                Municipio.activo == True).first()
        if datacreate:
            return HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="El Municipio ya existe")
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre de el Municipio se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        
        entity = Municipio(nombre=payload.nombre, codigo_dane=payload.codigo_dane,
                        id_departamento=payload.id_departamento, id_persona=tokenpayload.get("sub"), 
                                        activo=True, created_at=datetime.utcnow())
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        
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
    
    
    
    async def show(self, municipio_id: int):
        entity = self.db.query(Municipio).filter(
            Municipio.id == municipio_id,
                Municipio.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El Municipio no fue hallada")
        if municipio_id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo municipio_id se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    async def update_municipio(self, municipio_id: int, 
                            payload: MunicipioUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db.query(Municipio).filter(
            Municipio.id == municipio_id,
                Municipio.activo == True).first()
        if payload.nombre:
            existe = (
                self.db.query(Municipio)
                .filter(Municipio.nombre == payload.nombre, Municipio.id != municipio_id)
                .first()
            )
            if existe:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado por otro Municipio."
                )
        
        if not dataupdate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El Municipio no fue hallada")
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre de el Municipio se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
            
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")

        if dataupdate:
            dataupdate.nombre = payload.nombre
            dataupdate.codigo_dane = payload.codigo_dane
            dataupdate.id_departamento = payload.id_departamento
            dataupdate.id_persona = tokenpayload.get("sub")
            dataupdate.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(dataupdate)
            
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
    async def delete_municipio(self, municipio_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db.query(Municipio).filter(
            Municipio.id == municipio_id,
                Municipio.activo == True).first()
        if not datadelete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El Municipio no fue hallada")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
    # le paso un valor false para realizar un sofdelete para un eliminado logico
        datadelete.activo = False
        datadelete.deleted_at = datetime.utcnow()
        datadelete.id_persona = tokenpayload.get("sub")
        # guardar los cambios
        self.db.commit()
        self.db.refresh(datadelete)
        
        
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