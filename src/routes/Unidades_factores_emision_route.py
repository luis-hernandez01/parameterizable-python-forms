from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.config.config import (get_db, get_dbs)
from src.schemas.Unidades_factores_emision_schema import (
    UnidadFactorCreate,
    PaginacionSchema,
    UnidadFactorUpdate,
)
from src.services.unidades_factor_emision_services import UnidadfactorService
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


# mostrar todo 

@router.get("/all")
def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return UnidadfactorService(db).all()
    

# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def listar(
    activo: Optional[bool] = Query(True, description="Filtrar por activo (true o false)"),
    filtros: Optional[str] = Query(
        None,
        description="Filtrar por nombre (búsqueda parcial)"
    ),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = UnidadfactorService(db).lista(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = UnidadfactorService(db).count(activo=activo, filtros=filtros,)
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
def create(
    request: Request,
    payload: UnidadFactorCreate,
    # de esta manera llamo todas las bases de datos existentes
    dbs: list[Session] = Depends(get_dbs),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = UnidadfactorService(dbs).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{unidadfactor_id}")
def get_show(unidadfactor_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return UnidadfactorService(db).show(unidadfactor_id)


# endpoin para actualizar un registro x
@router.put("/{unidadfactor_id}")
def update_unidades(
    request: Request,
    unidadfactor_id: int,
    payload: UnidadFactorUpdate,
    # de esta manera llamo todas las bases de datos existentes
    dbs: list[Session] = Depends(get_dbs),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = UnidadfactorService(dbs).update(unidadfactor_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{unidadfactor_id}")
def delete(
    request: Request,
    unidadfactor_id: int,
    # de esta manera llamo todas las bases de datos existentes
    dbs: list[Session] = Depends(get_dbs),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = UnidadfactorService(dbs).delete(unidadfactor_id, request, tokenpayload)
    return {"data": result}



@router.post("/{unidadfactor_id}/reactivate")
def reactivates(request: Request, 
                        unidadfactor_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = UnidadfactorService(dbs).reactivate(unidadfactor_id, request, tokenpayload)
    return {"data": result}