from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.config.config import get_session
from src.services.clasificacion_services import clasificacionService
from src.schemas.clasificacion_proyecto_schema import (ClasificacionProyectoListResponse, 
                                                ClasificacionProyectoCreate,
                                                ClasificacionProyectoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

# endpoint de listar data con paginacion incluida
@router.get("/", response_model=ClasificacionProyectoListResponse)
def list_clasificaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    data = clasificacionService(db).list_clasificacion_proyecto(skip=skip, limit=limit)
    total = clasificacionService(db).count_clasificacion_proyecto()  
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
async def create_Clasificacion(request: Request, 
                        payload: ClasificacionProyectoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registrro con uan BD y esta dependencia se agregaria asi 
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    data = []
    
    for db in dbs:
        result = await clasificacionService(db).create_clacificacion_proyecto(payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}


# endpoint de show o ver registro
@router.get("/{clasificacion_id}")
async def get_show(clasificacion_id: int, db: Session = Depends(lambda: next(get_session(0)))):
    return await clasificacionService(db).show(clasificacion_id)


# endpoin para actualizar un registro x
@router.put("/{clasificacion_id}")
async def update_clasificacion(request: Request, 
                        clasificacion_id: int,
                        payload: ClasificacionProyectoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):

# crear registrro con uan BD y esta dependencia se agregaria asi 
# => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    
    data = []
    
    for db in dbs:
        result = await clasificacionService(db).update_clasificacion_pryecto(clasificacion_id, payload, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}


# endpoint para eliminar un registro logicamente
@router.delete("/{clasificacion_id}")
async def delete_clasificacion(request: Request, 
                        clasificacion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    data = []
    for db in dbs:
        result = await clasificacionService(db).delete_clasificacion(clasificacion_id, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}