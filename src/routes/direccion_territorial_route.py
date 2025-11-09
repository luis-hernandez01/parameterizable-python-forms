from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import get_session
from src.services.direccion_terrotorial_services import DireccionterritorialService
from src.schemas.direccionterritorial_schema import (PaginacionSchema, 
                                                DireccionTerritorialCreate,
                                                DireccionTerritorialUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
async def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return await DireccionterritorialService(db).all()



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def lista(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo (true o false)"),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = DireccionterritorialService(db).list_direccion(activo=activo, skip=skip, limit=limit)
    total = DireccionterritorialService(db).count_direccion(activo=activo)  
    # Método adicional para contar todos los datos
    return {
        "items": data,
        "per_page": per_page,
        "size": limit,
        "total": total,
        "last_page" : (total + per_page - 1) // per_page,
        "page": page,
        "pages": (total + limit - 1) // limit  # Redondeo hacia arriba
        
    }
    
    # endpoin de crear registro
@router.post("/")
async def creates(request: Request, 
                        payload: DireccionTerritorialCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await DireccionterritorialService(dbs).create_direccion(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{direccion_id}")
async def get_show(direccion_id: int, 
                db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return await DireccionterritorialService(db).show(direccion_id)


# endpoin para actualizar un registro x
@router.put("/{direccion_id}")
async def update(request: Request, 
                        direccion_id: int,
                        payload: DireccionTerritorialUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await DireccionterritorialService(dbs).update_direccion(direccion_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{direccion_id}")
async def delete(request: Request, 
                        direccion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await DireccionterritorialService(dbs).delete_direccion(direccion_id, request, tokenpayload)
    return {"data": result}


@router.post("/{direccion_id}/reactivate")
async def reactivates(request: Request, 
                        direccion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await DireccionterritorialService(dbs).reactivate(direccion_id, request, tokenpayload)
    return {"data": result}