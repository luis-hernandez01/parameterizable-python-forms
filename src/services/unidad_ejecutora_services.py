from datetime import datetime

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from src.models.logs_model import TipoOperacionEnum
from src.models.unidad_ejecutora_model import UnidadEjecutora
from src.schemas.unidad_ejecutora_schema import LogEntityRead, UnidadEjecutoraCreate
from src.utils.logs_util import LogUtil, registrar_log


# Servicio para listar las unidades de ejecucion
class UnidadEjecutoraService:
    def __init__(self, db: Session):
        self.db = db

    # servicio para listar  los registros
    def list_unidad_ejecutora(self, skip: int, limit: int):
        return (
            self.db.query(UnidadEjecutora)
            .filter(UnidadEjecutora.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_unidad_ejecutora(self):
        return (
            self.db.query(UnidadEjecutora)
            .filter(UnidadEjecutora.activo == True)
            .count()
        )

    # servicio para crear un registro
    async def create_unidad(
        self, payload: UnidadEjecutoraCreate, request: Request, tokenpayload: dict
    ):
        unidadcreate = (
            self.db.query(UnidadEjecutora)
            .filter(
                UnidadEjecutora.nombre == payload.nombre, UnidadEjecutora.activo == True
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

        entity = UnidadEjecutora(
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            id_persona=tokenpayload.get("sub"),
            activo=True,
            created_at=datetime.utcnow(),
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        # Registro de logs
        registrar_log(
            LogUtil(self.db),
            tabla_afectada="unidad_ejecutora",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1,
        )

        return LogEntityRead.from_orm(entity)

    async def show(self, unidad_id: int):
        entity = (
            self.db.query(UnidadEjecutora)
            .filter(UnidadEjecutora.id == unidad_id, UnidadEjecutora.activo == True)
            .first()
        )
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La unidad ejecutora no fue hallada",
            )
        if unidad_id == "":
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo unidad_id de la unidad ejecutora se encuentra vacia ingresa un dato valido",
            )
        return entity

    # servicio para editar logicamente un registro
    async def update_unidad(
        self,
        unidad_id: int,
        payload: UnidadEjecutoraCreate,
        request: Request,
        tokenpayload: dict,
    ):
        dataupdate = (
            self.db.query(UnidadEjecutora)
            .filter(UnidadEjecutora.id == unidad_id, UnidadEjecutora.activo == True)
            .first()
        )
        if payload.nombre:
            existe = (
                self.db.query(UnidadEjecutora)
                .filter(
                    UnidadEjecutora.nombre == payload.nombre,
                    UnidadEjecutora.id != unidad_id,
                )
                .first()
            )
            if existe:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado por otra unidad ejecutora.",
                )

        if not dataupdate:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La unidad ejecutora no fue hallada",
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

        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")

        if dataupdate:
            dataupdate.nombre = payload.nombre
            dataupdate.descripcion = payload.descripcion
            dataupdate.id_persona = tokenpayload.get("sub")
            dataupdate.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(dataupdate)

            # Registro de logs
        registrar_log(
            LogUtil(self.db),
            tabla_afectada="unidad_ejecutora",
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
    async def delete_unidad(self, unidad_id: int, request: Request, tokenpayload: dict):
        datadelete = (
            self.db.query(UnidadEjecutora)
            .filter(UnidadEjecutora.id == unidad_id, UnidadEjecutora.activo == True)
            .first()
        )
        if not datadelete:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La unidad ejecutora no fue hallada",
            )

        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
        # le paso un valor false para realizar un sofdelete para un eliminado logico
        datadelete.activo = False
        datadelete.deleted_at = datetime.utcnow()
        datadelete.id_persona = tokenpayload.get("sub")
        # guardar los cambios
        self.db.commit()
        self.db.refresh(datadelete)

        registrar_log(
            LogUtil(self.db),
            tabla_afectada="unidad_ejecutora",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1,
        )

        return LogEntityRead.from_orm(datadelete)
