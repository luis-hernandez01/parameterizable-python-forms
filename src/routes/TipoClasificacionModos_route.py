from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db, get_dbs)
from src.services.TipoClasificacionModos_services import TipoClasificacionModosService
from src.schemas.TipoClasificacionModos_schema import (PaginacionSchema, 
                                                TipoClasificacionModosCreate,
                                                TipoClasificacionModosUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


@router.get("/all")
def list_all(
    # de esta manera llamo solamente la primera base de datos
    id_modo: int,
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return TipoClasificacionModosService(db).all(id_modo)



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def listar(
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
    data = TipoClasificacionModosService(db).list_tipo_clasificacion(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = TipoClasificacionModosService(db).count_tipo_clasificacion(activo=activo, filtros=filtros)  
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
def create(request: Request, 
                        payload: TipoClasificacionModosCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)
                        # tokenpayload: dict = {"sub": 2}
                        ):
    result = TipoClasificacionModosService(dbs).create_tipo_clasificacion(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{tipo_clasificacion_id}")
def get_show(tipo_clasificacion_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return TipoClasificacionModosService(db).show(tipo_clasificacion_id)


# endpoin para actualizar un registro x
@router.put("/{tipo_clasificacion_id}")
def update_unidades(request: Request, 
                        tipo_clasificacion_id: int,
                        payload: TipoClasificacionModosUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TipoClasificacionModosService(dbs).update_tipo_clasificacion(tipo_clasificacion_id, payload, request, tokenpayload)
    return {"data": result}
    


# endpoint para eliminar un registro logicamente
@router.delete("/{tipo_clasificacion_id}")
def delete(request: Request, 
                        tipo_clasificacion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TipoClasificacionModosService(dbs).delete_tipo_clasificacion(tipo_clasificacion_id, request, tokenpayload)
    return {"data": result}


@router.post("/{tipo_clasificacion_id}/reactivate")
def reactivates(request: Request, 
                        tipo_clasificacion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TipoClasificacionModosService(dbs).reactivate(tipo_clasificacion_id, request, tokenpayload)
    return {"data": result}