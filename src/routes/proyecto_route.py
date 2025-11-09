from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import get_session
from src.services.proyecto_services import ProyectoService
from src.schemas.proyecto_schema import (PaginacionSchema, 
                                                proyectoCreate,
                                                ProyectoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


@router.get("/all")
async def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return await ProyectoService(db).all()



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def lista(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo (true o false)"),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0)))
    
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = ProyectoService(db).list_proyecto(activo=activo, skip=skip, limit=limit)
    total = ProyectoService(db).count_proyecto(activo=activo)  
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
                        payload: proyectoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await ProyectoService(dbs).create_proyecto(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{proyecto_id}")
async def get_show(proyecto_id: int, 
                db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return await ProyectoService(db).show(proyecto_id)


# endpoin para actualizar un registro x
@router.put("/{proyecto_id}")
async def update(request: Request, 
                        proyecto_id: int,
                        payload: ProyectoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await ProyectoService(dbs).update_proyecto(proyecto_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{proyecto_id}")
async def delete(request: Request, 
                        proyecto_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await ProyectoService(dbs).delete_proyecto(proyecto_id, request, tokenpayload)
    return {"data": result}


@router.post("/{proyecto_id}/reactivate")
async def reactivates(request: Request, 
                        proyecto_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = await ProyectoService(dbs).reactivate(proyecto_id, request, tokenpayload)
    return {"data": result}