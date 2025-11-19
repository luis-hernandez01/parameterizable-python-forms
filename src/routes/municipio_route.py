from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db, get_dbs)
from src.services.municipio_services import MunicipioService
from src.schemas.municipio_schema import (PaginacionSchema, 
                                                municipioCreate,
                                                MunicipioUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
def list_all( codigo_departamento: str,
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return MunicipioService(db).all(codigo_departamento)


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
    data = MunicipioService(db).list_municipio(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = MunicipioService(db).count_municipio(activo=activo, filtros=filtros)  
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
                        payload: municipioCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = MunicipioService(dbs).create_municipio(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{municipio_id}")
def get_show(municipio_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return MunicipioService(db).show(municipio_id)


# endpoin para actualizar un registro x
@router.put("/{municipio_id}")
def update(request: Request, 
                        municipio_id: int,
                        payload: MunicipioUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = MunicipioService(dbs).update_municipio(municipio_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{municipio_id}")
def delete(request: Request, 
                        municipio_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = MunicipioService(dbs).delete_municipio(municipio_id, request, tokenpayload)
    return {"data": result}


@router.post("/{municipio_id}/reactivate")
def reactivates(request: Request, 
                        municipio_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = MunicipioService(dbs).reactivate(municipio_id, request, tokenpayload)
    return {"data": result}