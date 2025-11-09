from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import get_session
from src.services.tramo_services import TramoService
from src.schemas.tramos_sectores_schema import (PaginacionSchema, 
                                                TramoCreate,
                                                TramoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
async def list_all(
    # de esta manera llamo solamente la primera base de datos
    id_ruta: int,
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return await TramoService(db).all(id_ruta)



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def lista(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo (true o false)"),
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = TramoService(db).list_tramo(activo=activo, skip=skip, limit=limit)
    total = TramoService(db).count_tramo(activo=activo)  
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
                        payload: TramoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await TramoService(dbs).create_tramo(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{tramo_id}")
async def get_show(tramo_id: int,
                db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return await TramoService(db).show(tramo_id)


# endpoin para actualizar un registro x
@router.put("/{tramo_id}")
async def update(request: Request, 
                        tramo_id: int,
                        payload: TramoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await TramoService(dbs).update_tramo(tramo_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{tramo_id}")
async def delete(request: Request, 
                        tramo_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await TramoService(dbs).delete_tramo(tramo_id, request, tokenpayload)
    return {"data": result}



@router.post("/{tramo_id}/reactivate")
async def reactivates(request: Request, 
                        tramo_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await TramoService(dbs).reactivate(tramo_id, request, tokenpayload)
    return {"data": result}