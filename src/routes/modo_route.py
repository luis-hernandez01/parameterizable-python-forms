from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db, get_dbs)
from src.services.modo_services import ModoService
from src.schemas.modo_schema import (PaginacionSchema, 
                                                ModoCreate,
                                                ModoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return ModoService(db).all()



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def lista(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    activo: Optional[bool] = Query(True, description="Filtrar por estado activo (true o false)"),
    filtros: Optional[str] = Query(
        None,
        description="Filtrar por nombre (búsqueda parcial)"
    ),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = ModoService(db).list_modo(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = ModoService(db).count_modo(activo=activo, filtros=filtros)  
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
def creates(request: Request, 
                        payload: ModoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = ModoService(dbs).create_modo(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{modo_id}")
def get_show(modo_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return ModoService(db).show(modo_id)


# endpoin para actualizar un registro x
@router.put("/{modo_id}")
def update(request: Request, 
                        modo_id: int,
                        payload: ModoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = ModoService(dbs).update_modo(modo_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{modo_id}")
def delete(request: Request, 
                        modo_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = ModoService(dbs).delete_modo(modo_id, request, tokenpayload)
    return {"data": result}


@router.post("/{modo_id}/reactivate")
def reactivates(request: Request, 
                        modo_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = ModoService(dbs).reactivate(modo_id, request, tokenpayload)
    return {"data": result}