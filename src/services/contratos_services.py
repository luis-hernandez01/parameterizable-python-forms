from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.contratos_model import Contrato
from src.models.logs_model import TipoOperacionEnum
from src.schemas.contratos_schema import ContratoCreate, ContratoUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import registrar_log, LogUtil

# Servicio para listar las unidades de ejecucion
class ContratoService:
    def __init__(self, db: Session):
        self.db = db
        
    async def all(self):
        return (
            self.db.query(Contrato)
            .filter(Contrato.activo == True)
            .all()
        )
        
# servicio para listar  los registros
    def list_contrato(self, skip: int, limit: int):
        return self.db.query(Contrato).filter(Contrato.activo == True).offset(skip).limit(limit).all()
    def count_contrato(self):
        return self.db.query(Contrato).filter(Contrato.activo == True).count()
    
    
    # servicio para crear un registro
    async def create_contrato(self, payload: ContratoCreate, 
                            request: Request, tokenpayload: dict):
        datacreate = self.db.query(Contrato).filter(
            Contrato.numero_contrato == payload.numero_contrato,
                Contrato.activo == True).first()
        if datacreate:
            return HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="El numero de contrato ya existe")
        if payload.numero_contrato =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre se encuentra vacia ingresa un dato valido")
        if len(payload.numero_contrato) > 100:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo numero contrato no puede tener un rango mayor a 100 caracteres")
        
        if payload.numero_contrato =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre de el modo se encuentra vacia ingresa un dato valido")
        
        data = payload.model_dump()
        
        try:
            for key in [
                "id_proyecto",
            ]:
                if data.get(key) == 0:
                    data[key] = None
                    
            data["activo"] = True
            data["id_persona"] = tokenpayload.get("sub")
            data["created_at"] = datetime.utcnow()
            entity = Contrato(**data)
            
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            self.db.rollback()
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error creando el contrato: {e}")
        
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="contrato",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
    
    
    
    async def show(self, contrato_id: int):
        entity = self.db.query(Contrato).filter(
            Contrato.id == contrato_id,
                Contrato.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El contrato no fue hallada")
        if Contrato =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo Contrato se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    async def update_contrato(self, contrato_id: int, 
                            payload: ContratoUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db.query(Contrato).filter(
            Contrato.id == contrato_id,
                Contrato.activo == True).first()
        if payload.numero_contrato:
            existe = (
                self.db.query(Contrato)
                .filter(Contrato.numero_contrato == payload.numero_contrato, Contrato.id != contrato_id)
                .first()
            )
            if existe:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El numero '{payload.numero_contrato}' ya está siendo usado por otro contrato."
                )
        
        if not dataupdate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El contrato no fue hallada")
        if payload.numero_contrato =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo numero de contrato se encuentra vacia ingresa un dato valido")
        if len(payload.numero_contrato) > 100:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo numero de contrato no puede tener un rango mayor a 100 caracteres")
            
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")

        if dataupdate:
            
            for field, value in payload.model_dump(exclude_unset=True).items():
                # 🔍 Convierte automáticamente valores 0 en None para claves foráneas
                if field in [
                    "id_proyecto",
                ] and value == 0:
                    value = None

                setattr(dataupdate, field, value)
                
                #  Campos de auditoría
            dataupdate.id_persona = tokenpayload.get("sub")
            dataupdate.updated_at = datetime.utcnow()
            
            # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="contrato",
            id_registro_afectado=dataupdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataupdate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=dataupdate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(dataupdate)
    
    
    # servicio para eliminar logicamente un registro
    async def delete_contrato(self, contrato_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db.query(Contrato).filter(
            Contrato.id == contrato_id,
                Contrato.activo == True).first()
        if not datadelete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El contrato no fue hallado")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
    # le paso un valor false para realizar un sofdelete para un eliminado logico
        datadelete.activo = False
        datadelete.deleted_at = datetime.utcnow()
        datadelete.id_persona = tokenpayload.get("sub")
        # guardar los cambios
        self.db.commit()
        self.db.refresh(datadelete)
        
        
        registrar_log(LogUtil(self.db),
            tabla_afectada="contrato",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datadelete)