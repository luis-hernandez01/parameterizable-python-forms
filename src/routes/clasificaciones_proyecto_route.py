from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db, get_dbs)
from src.services.clasificacion_services import clasificacionService
from src.schemas.clasificacion_proyecto_schema import (PaginacionSchema, 
                                                ClasificacionProyectoCreate,
                                                ClasificacionProyectoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


@router.get("/all")
def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return clasificacionService(db).all()



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def list_clasificaciones(
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
    data = clasificacionService(db).list_clasificacion_proyecto(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = clasificacionService(db).count_clasificacion_proyecto(activo=activo, filtros=filtros)  
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
def create_Clasificacion(request: Request, 
                        payload: ClasificacionProyectoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = clasificacionService(dbs).create_clacificacion_proyecto(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{clasificacion_id}")
def get_show(clasificacion_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return clasificacionService(db).show(clasificacion_id)


# endpoin para actualizar un registro x
@router.put("/{clasificacion_id}")
def update_clasificacion(request: Request, 
                        clasificacion_id: int,
                        payload: ClasificacionProyectoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = clasificacionService(dbs).update_clasificacion_pryecto(clasificacion_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{clasificacion_id}")
def delete_clasificacion(request: Request, 
                        clasificacion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = clasificacionService(dbs).delete_clasificacion(clasificacion_id, request, tokenpayload)
    return {"data": result}


@router.post("/{clasificacion_id}/reactivate")
def reactivates(request: Request, 
                        clasificacion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = clasificacionService(dbs).reactivate(clasificacion_id, request, tokenpayload)
    return {"data": result}