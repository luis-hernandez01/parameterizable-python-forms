from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.config.config import get_session
from src.services.TipoClasificacionModos_services import TipoClasificacionModosService
from src.schemas.TipoClasificacionModos_schema import (TipoClasificacionListResponse, 
                                                TipoClasificacionModosCreate,
                                                TipoClasificacionModosUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


@router.get("/all")
async def list_all(
    # de esta manera llamo solamente la primera base de datos
    id_modo: int,
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return await TipoClasificacionModosService(db).all(id_modo)



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=TipoClasificacionListResponse)
def listar(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    data = TipoClasificacionModosService(db).list_tipo_clasificacion(skip=skip, limit=limit)
    total = TipoClasificacionModosService(db).count_tipo_clasificacion()  
    # Método adicional para contar todos los datos
    return {
        "data": data,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": total,
            "page": (skip // limit) + 1,
            "pages": (total + limit - 1) // limit  # Redondeo hacia arriba
        }
    }
    
    # endpoin de crear registro
@router.post("/")
async def create(request: Request, 
                        payload: TipoClasificacionModosCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)
                        # tokenpayload: dict = {"sub": 2}
                        ):
    
    # crear registrro con uan BD y esta dependencia se agregaria asi 
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    data = []
    
    for db in dbs:
        result = await TipoClasificacionModosService(db).create_tipo_clasificacion(payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}


# endpoint de show o ver registro
@router.get("/{tipo_clasificacion_id}")
async def get_show(tipo_clasificacion_id: int, 
                db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return await TipoClasificacionModosService(db).show(tipo_clasificacion_id)


# endpoin para actualizar un registro x
@router.put("/{tipo_clasificacion_id}")
async def update_unidades(request: Request, 
                        tipo_clasificacion_id: int,
                        payload: TipoClasificacionModosUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):

# crear registrro con uan BD y esta dependencia se agregaria asi 
# => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    
    data = []
    
    for db in dbs:
        result = await TipoClasificacionModosService(db).update_tipo_clasificacion(tipo_clasificacion_id, payload, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}


# endpoint para eliminar un registro logicamente
@router.delete("/{tipo_clasificacion_id}")
async def delete(request: Request, 
                        tipo_clasificacion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    data = []
    for db in dbs:
        result = await TipoClasificacionModosService(db).delete_tipo_clasificacion(tipo_clasificacion_id, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}