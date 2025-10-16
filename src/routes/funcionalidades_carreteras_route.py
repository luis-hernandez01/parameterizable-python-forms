from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.config.config import get_session
from src.services.funcionalidades_services import FuncionalidadesCarreterService
from src.schemas.funcionalidades_carretera_schema import (FuncionalidadesListResponse, 
                                                funcionalidades_carreteraCreate,
                                                funcionalidades_carreteraUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

# endpoint de listar data con paginacion incluida
@router.get("/", response_model=FuncionalidadesListResponse)
def list_funcionalidades(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    data = FuncionalidadesCarreterService(db).list_funcionalidades_carretera(skip=skip, limit=limit)
    total = FuncionalidadesCarreterService(db).count_funcionalidades_carretera()  
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
async def create_funcionalidades(request: Request, 
                        payload: funcionalidades_carreteraCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registrro con uan BD y esta dependencia se agregaria asi 
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    data = []
    
    for db in dbs:
        result = await FuncionalidadesCarreterService(db).create_funcionalidades_carretera(payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}


# endpoint de show o ver registro
@router.get("/{funcionalidades_id}")
async def get_show(funcionalidades_id: int, db: Session = Depends(lambda: next(get_session(0)))):
    return await FuncionalidadesCarreterService(db).show(funcionalidades_id)


# endpoin para actualizar un registro x
@router.put("/{funcionalidades_id}")
async def update_unidades(request: Request, 
                        funcionalidades_id: int,
                        payload: funcionalidades_carreteraUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):

# crear registrro con uan BD y esta dependencia se agregaria asi 
# => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    
    data = []
    
    for db in dbs:
        result = await FuncionalidadesCarreterService(db).update_funcionalidades(funcionalidades_id, payload, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}


# endpoint para eliminar un registro logicamente
@router.delete("/{funcionalidades_id}")
async def delete(request: Request, 
                        funcionalidades_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    data = []
    for db in dbs:
        result = await FuncionalidadesCarreterService(db).delete_funcionalidad(funcionalidades_id, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}
