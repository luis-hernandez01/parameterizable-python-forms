from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.config.config import get_session
from src.services.contratos_services import ContratoService
from src.schemas.contratos_schema import (ContratoListResponse, 
                                                ContratoCreate,
                                                ContratoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

# endpoint de listar data con paginacion incluida
@router.get("/", response_model=ContratoListResponse)
def lista(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    data = ContratoService(db).list_contrato(skip=skip, limit=limit)
    total = ContratoService(db).count_contrato()  
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
                        payload: ContratoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registrro con uan BD y esta dependencia se agregaria asi 
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    data = []
    
    for db in dbs:
        result = await ContratoService(db).create_contrato(payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}


# endpoint de show o ver registro
@router.get("/{contrato_id}")
async def get_show(contrato_id: int, db: Session = Depends(lambda: next(get_session(0)))):
    return await ContratoService(db).show(contrato_id)


# endpoin para actualizar un registro x
@router.put("/{contrato_id}")
async def update(request: Request, 
                        contrato_id: int,
                        payload: ContratoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):

# crear registrro con uan BD y esta dependencia se agregaria asi 
# => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    
    data = []
    
    for db in dbs:
        result = await ContratoService(db).update_contrato(contrato_id, payload, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}


# endpoint para eliminar un registro logicamente
@router.delete("/{contrato_id}")
async def delete(request: Request, 
                        contrato_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    data = []
    for db in dbs:
        result = await ContratoService(db).delete_contrato(contrato_id, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}
