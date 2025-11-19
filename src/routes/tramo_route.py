from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db, get_dbs)
from src.services.tramo_services import TramoService
from src.schemas.tramos_sectores_schema import (PaginacionSchema, 
                                                TramoCreate,
                                                TramoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/all")
def list_all(
    # de esta manera llamo solamente la primera base de datos
    id_ruta: int,
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return TramoService(db).all(id_ruta)



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def lista(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    activo: Optional[bool] = Query(True, description="Filtrar por estado activo (true o false)"),
    filtros: Optional[str] = Query(
        None,
        description="Filtrar por nombre (búsqueda parcial)"
    ),
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = TramoService(db).list_tramo(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = TramoService(db).count_tramo(activo=activo, filtros=filtros)  
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
                        payload: TramoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TramoService(dbs).create_tramo(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{tramo_id}")
def get_show(tramo_id: int,
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return TramoService(db).show(tramo_id)


# endpoin para actualizar un registro x
@router.put("/{tramo_id}")
def update(request: Request, 
                        tramo_id: int,
                        payload: TramoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TramoService(dbs).update_tramo(tramo_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{tramo_id}")
def delete(request: Request, 
                        tramo_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TramoService(dbs).delete_tramo(tramo_id, request, tokenpayload)
    return {"data": result}



@router.post("/{tramo_id}/reactivate")
def reactivates(request: Request, 
                        tramo_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TramoService(dbs).reactivate(tramo_id, request, tokenpayload)
    return {"data": result}