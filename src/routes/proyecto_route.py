from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.config.config import get_session
from src.services.proyecto_services import ProyectoService
from src.schemas.proyecto_schema import (ProyectoListResponse, 
                                                proyectoCreate,
                                                ProyectoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


@router.get("/all")
async def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return await ProyectoService(db).all()



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=ProyectoListResponse)
def lista(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0)))
    
) -> Dict[str, Any]:
    data = ProyectoService(db).list_proyecto(skip=skip, limit=limit)
    total = ProyectoService(db).count_proyecto()  
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
async def creates(request: Request, 
                        payload: proyectoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registrro con uan BD y esta dependencia se agregaria asi 
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    data = []
    
    for db in dbs:
        result = await ProyectoService(db).create_proyecto(payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}


# endpoint de show o ver registro
@router.get("/{proyecto_id}")
async def get_show(proyecto_id: int, db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return await ProyectoService(db).show(proyecto_id)


# endpoin para actualizar un registro x
@router.put("/{proyecto_id}")
async def update(request: Request, 
                        proyecto_id: int,
                        payload: ProyectoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):

# crear registrro con uan BD y esta dependencia se agregaria asi 
# => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    
    data = []
    
    for db in dbs:
        result = await ProyectoService(db).update_proyecto(proyecto_id, payload, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}


# endpoint para eliminar un registro logicamente
@router.delete("/{proyecto_id}")
async def delete(request: Request, 
                        proyecto_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    data = []
    for db in dbs:
        result = await ProyectoService(db).delete_proyecto(proyecto_id, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}
