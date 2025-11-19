from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db, get_dbs)
from src.services.contratos_services import ContratoService
from src.schemas.contratos_schema import (PaginacionSchema, 
                                                ContratoCreate,
                                                ContratoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


@router.get("/all")
def list_all(
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return ContratoService(db).all()



# endpoint de listar data con paginacion incluida
@router.get("/", response_model=PaginacionSchema)
def lista(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    activo: Optional[bool] = Query(True, description="Filtrar por estado activo (true o false)"),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = ContratoService(db).list_contrato(activo=activo, skip=skip, limit=limit)
    total = ContratoService(db).count_contrato(activo=activo)  
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
                        payload: ContratoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = ContratoService(dbs).create_contrato(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{contrato_id}")
def get_show(contrato_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return ContratoService(db).show(contrato_id)


# endpoin para actualizar un registro x
@router.put("/{contrato_id}")
def update(request: Request, 
                        contrato_id: int,
                        payload: ContratoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = ContratoService(dbs).update_contrato(contrato_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{contrato_id}")
def delete(request: Request, 
                        contrato_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = ContratoService(dbs).delete_contrato(contrato_id, request, tokenpayload)
    return {"data": result}


@router.post("/{contrato_id}/reactivate")
def reactivates(request: Request, 
                        contrato_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(get_dbs),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = ContratoService(dbs).reactivate(contrato_id, request, tokenpayload)
    return {"data": result}