from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db, get_dbs)
from src.services.catalogo_services import catalogoService
from src.schemas.catalogomodoXtipoclasificacion_schema import (PaginacionSchema, 
                                                CatalogoCreate,
                                                CatalogoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
def list_all(
    # de esta manera llamo solamente la primera base de datos
    id_modo: int, id_tipo: int,
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return catalogoService(db).all(id_modo, id_tipo)


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
    data = catalogoService(db).list_catalogo(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = catalogoService(db).count_catalogo(activo=activo, filtros=filtros)  
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
                        payload: CatalogoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)
                        # tokenpayload: dict = {"sub": 2}
                        ):
    result = catalogoService(dbs).create_catalogo(payload, request, tokenpayload)
    return {"data": result}

# @router.post("/")
# def creates(request: Request, 
#                         payload: CatalogoCreate, 
#                         # de esta manera llamo todas las bases de datos existentes
#                         # dbs: list[Session] = Depends(get_dbs),
#                         dbs: Session = Depends(get_session),
#                         tokenpayload: dict = Depends(verify_jwt_token)
#                         # tokenpayload: dict = {"sub": 2}
#                         ):
    
#     result = catalogoService(dbs).create_catalogo(payload, request, tokenpayload)
#     return {"data": result}


# endpoint de show o ver registro
@router.get("/{catalogo_id}")
def get_show(catalogo_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return catalogoService(db).show(catalogo_id)


# endpoin para actualizar un registro x
@router.put("/{catalogo_id}")
def update(request: Request, 
                        catalogo_id: int,
                        payload: CatalogoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = catalogoService(dbs).update_catalogo(catalogo_id,payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{catalogo_id}")
def delete(request: Request, 
                        catalogo_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = catalogoService(dbs).delete_catalogo(catalogo_id, request, tokenpayload)
    return {"data": result}

@router.post("/{catalogo_id}/reactivate")
def reactivates(request: Request, 
                        catalogo_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = catalogoService(dbs).reactivate(catalogo_id, request, tokenpayload)
    return {"data": result}
