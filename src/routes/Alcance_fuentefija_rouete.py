from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import get_session
from src.services.alcance_services import AlcanceService
from src.schemas.Alcance_fuentefija_schema import (PaginacionSchema, 
                                                AlcanceCreate,
                                                AlcanceUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
async def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return await AlcanceService(db).all()


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
    data = AlcanceService(db).listar(activo=activo, skip=skip, limit=limit)
    total = AlcanceService(db).count(activo=activo)  
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
                        payload: AlcanceCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await AlcanceService(dbs).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{alcance_id}")
async def get_show(alcance_id: int, 
                db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return await AlcanceService(db).show(alcance_id)


# endpoin para actualizar un registro x
@router.put("/{alcance_id}")
async def update(request: Request, 
                        alcance_id: int,
                        payload: AlcanceUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await AlcanceService(dbs).updates(alcance_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{alcance_id}")
async def delete(request: Request, 
                        alcance_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await AlcanceService(dbs).deletes(alcance_id, request, tokenpayload)
    return {"data": result}


@router.post("/{alcance_id}/reactivate")
async def reactivates(request: Request, 
                        alcance_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await AlcanceService(dbs).reactivate(alcance_id, request, tokenpayload)
    return {"data": result}