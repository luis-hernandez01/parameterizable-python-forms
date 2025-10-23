from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.Proyecto_model import Proyecto
from src.models.logs_model import TipoOperacionEnum
from src.schemas.proyecto_schema import proyectoCreate, ProyectoUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import registrar_log, LogUtil

# Servicio para listar las unidades de ejecucion
class ProyectoService:
    def __init__(self, db: Session):
        self.db = db
        
# servicio para listar  los registros
    def list_proyecto(self, skip: int, limit: int):
        return self.db.query(Proyecto).filter(Proyecto.activo == True).offset(skip).limit(limit).all()
    def count_proyecto(self):
        return self.db.query(Proyecto).filter(Proyecto.activo == True).count()
    
    
    # servicio para crear un registro
    async def create_proyecto(self, payload: proyectoCreate, 
                            request: Request, tokenpayload: dict):
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
                "id_funcionalidad",
                "id_categorizacion",
            ]:
                if data.get(key) == 0:
                    data[key] = None
                    
            data["activo"] = True
            data["id_persona"] = tokenpayload.get("sub")
            data["created_at"] = datetime.utcnow()
            entity = Proyecto(**data)
            
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            self.db.rollback()
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error creando el proyecto: {e}")
        
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
    
    
    
    async def show(self, proyecto_id: int):
        entity = self.db.query(Proyecto).filter(
            Proyecto.id == proyecto_id,
                Proyecto.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto no fue hallada")
        if proyecto_id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo proyecto_id se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    async def update_proyecto(self, proyecto_id: int, 
                            payload: ProyectoUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db.query(Proyecto).filter(
            Proyecto.id == proyecto_id,
                Proyecto.activo == True).first()
        
        if not dataupdate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto no fue hallada")
        
            
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")

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
                    "id_funcionalidad",
                    "id_categorizacion",
                ] and value == 0:
                    value = None

                setattr(dataupdate, field, value)

            #  Campos de auditoría
            dataupdate.id_persona = tokenpayload.get("sub")
            dataupdate.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(dataupdate)
            
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
    async def delete_proyecto(self, proyecto_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db.query(Proyecto).filter(
            Proyecto.id == proyecto_id,
                Proyecto.activo == True).first()
        if not datadelete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto no fue hallada")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
    # le paso un valor false para realizar un sofdelete para un eliminado logico
        datadelete.activo = False
        datadelete.deleted_at = datetime.utcnow()
        datadelete.id_persona = tokenpayload.get("sub")
        # guardar los cambios
        self.db.commit()
        self.db.refresh(datadelete)
        
        
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