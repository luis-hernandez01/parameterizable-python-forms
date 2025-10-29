from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.config.config import get_session
from src.services.trimestre_services import TrimestreService
from src.schemas.trimestre_schema import (TrimestreListResponse, 
                                                TrimestreCreate,
                                                TrimestreUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
async def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return await TrimestreService(db).all()

# endpoint de listar data con paginacion incluida
@router.get("/", response_model=TrimestreListResponse)
def lista(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    data = TrimestreService(db).listar(skip=skip, limit=limit)
    total = TrimestreService(db).count()  
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
                        payload: TrimestreCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registrro con uan BD y esta dependencia se agregaria asi 
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    data = []
    
    for db in dbs:
        result = await TrimestreService(db).create(payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}


# endpoint de show o ver registro
@router.get("/{trimestre_id}")
async def get_show(trimestre_id: int, 
                db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return await TrimestreService(db).show(trimestre_id)


# endpoin para actualizar un registro x
@router.put("/{trimestre_id}")
async def update(request: Request, 
                        trimestre_id: int,
                        payload: TrimestreUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):

# crear registrro con uan BD y esta dependencia se agregaria asi 
# => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    
    data = []
    
    for db in dbs:
        result = await TrimestreService(db).updates(trimestre_id, payload, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}


# endpoint para eliminar un registro logicamente
@router.delete("/{trimestre_id}")
async def delete(request: Request, 
                        trimestre_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    data = []
    for db in dbs:
        result = await TrimestreService(db).delete_modo(trimestre_id, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}
