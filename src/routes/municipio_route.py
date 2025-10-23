from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.config.config import get_session
from src.services.municipio_services import MunicipioService
from src.schemas.municipio_schema import (municipioListResponse, 
                                                municipioCreate,
                                                MunicipioUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
async def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return await MunicipioService(db).all()

# endpoint de listar data con paginacion incluida
@router.get("/", response_model=municipioListResponse)
def lista(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    data = MunicipioService(db).list_municipio(skip=skip, limit=limit)
    total = MunicipioService(db).count_municipio()  
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
                        payload: municipioCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registrro con uan BD y esta dependencia se agregaria asi 
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    data = []
    
    for db in dbs:
        result = await MunicipioService(db).create_municipio(payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}


# endpoint de show o ver registro
@router.get("/{municipio_id}")
async def get_show(municipio_id: int, db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return await MunicipioService(db).show(municipio_id)


# endpoin para actualizar un registro x
@router.put("/{municipio_id}")
async def update(request: Request, 
                        municipio_id: int,
                        payload: MunicipioUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):

# crear registrro con uan BD y esta dependencia se agregaria asi 
# => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    
    data = []
    
    for db in dbs:
        result = await MunicipioService(db).update_municipio(municipio_id, payload, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}


# endpoint para eliminar un registro logicamente
@router.delete("/{municipio_id}")
async def delete(request: Request, 
                        municipio_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    data = []
    for db in dbs:
        result = await MunicipioService(db).delete_municipio(municipio_id, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}
