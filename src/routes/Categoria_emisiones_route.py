from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.config.config import get_session
from src.schemas.Categoria_emisiones_schema import (
    CategoriaCreate,
    PaginacionSchema,
    CategoriaUpdate,
)
from src.services.categoria_emision_services import CategoriaService
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


# mostrar todo 

@router.get("/all")
async def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return await CategoriaService(db).all()
    

# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def listar(
    activo: Optional[bool] = Query(None, description="Filtrar por activo (true o false)"),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = CategoriaService(db).lista(activo=activo, skip=skip, limit=limit)
    total = CategoriaService(db).count(activo=activo)
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
async def create(
    request: Request,
    payload: CategoriaCreate,
    # de esta manera llamo todas las bases de datos existentes
    dbs: list[Session] = Depends(lambda: next(get_session())),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = await CategoriaService(dbs).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{categoria_id}")
async def get_show(categoria_id: int, 
                db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return await CategoriaService(db).show(categoria_id)


# endpoin para actualizar un registro x
@router.put("/{categoria_id}")
async def update_unidades(
    request: Request,
    categoria_id: int,
    payload: CategoriaUpdate,
    # de esta manera llamo todas las bases de datos existentes
    dbs: list[Session] = Depends(lambda: next(get_session())),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = await CategoriaService(dbs).update(categoria_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{categoria_id}")
async def delete_unidades(
    request: Request,
    categoria_id: int,
    # de esta manera llamo todas las bases de datos existentes
    dbs: list[Session] = Depends(lambda: next(get_session())),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = await CategoriaService(dbs).delete(categoria_id, request, tokenpayload)
    return {"data": result}



@router.post("/{categoria_id}/reactivate")
async def reactivates(request: Request, 
                        categoria_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await CategoriaService(dbs).reactivate(categoria_id, request, tokenpayload)
    return {"data": result}