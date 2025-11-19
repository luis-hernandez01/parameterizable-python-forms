from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db, get_dbs)
from src.services.categoria_fuentesfijas_services import Categoria_fuentesfijas_Service
from src.schemas.Categoria_fuentefija_schema import (PaginacionSchema, 
                                                Categoria_fCreate,
                                                Categoria_fUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return Categoria_fuentesfijas_Service(db).all()


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
    data = Categoria_fuentesfijas_Service(db).listar(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = Categoria_fuentesfijas_Service(db).count(activo=activo, filtros=filtros)  
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
                        payload: Categoria_fCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Categoria_fuentesfijas_Service(dbs).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{categoria_id}")
def get_show(categoria_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return Categoria_fuentesfijas_Service(db).show(categoria_id)


# endpoin para actualizar un registro x
@router.put("/{categoria_id}")
def update(request: Request, 
                        categoria_id: int,
                        payload: Categoria_fUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Categoria_fuentesfijas_Service(dbs).updates(categoria_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{categoria_id}")
def delete(request: Request, 
                        categoria_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Categoria_fuentesfijas_Service(dbs).deletes(categoria_id, request, tokenpayload)
    return {"data": result}


@router.post("/{categoria_id}/reactivate")
def reactivates(request: Request, 
                        categoria_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Categoria_fuentesfijas_Service(dbs).reactivate(categoria_id, request, tokenpayload)
    return {"data": result}