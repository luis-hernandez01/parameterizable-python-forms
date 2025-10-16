from typing import Any, Dict

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.config.config import get_session
from src.schemas.unidad_ejecutora_schema import (
    UnidadEjecutoraCreate,
    UnidadEjecutoraListResponse,
    UnidadEjecutoraUpdate,
)
from src.services.unidad_ejecutora_services import UnidadEjecutoraService
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


# endpoint de listar data con paginacion incluida
@router.get("/", response_model=UnidadEjecutoraListResponse)
def list_unidades(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
) -> Dict[str, Any]:
    data = UnidadEjecutoraService(db).list_unidad_ejecutora(skip=skip, limit=limit)
    total = UnidadEjecutoraService(db).count_unidad_ejecutora()
    # Método adicional para contar todos los datos
    return {
        "data": data,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": total,
            "page": (skip // limit) + 1,
            "pages": (total + limit - 1) // limit,  # Redondeo hacia arriba
        },
    }

    # endpoin de crear registro


@router.post("/")
async def create_unidades(
    request: Request,
    payload: UnidadEjecutoraCreate,
    # de esta manera llamo todas las bases de datos existentes
    dbs: list[Session] = Depends(lambda: next(get_session())),
    tokenpayload: dict = Depends(verify_jwt_token),
):

    # crear registrro con uan BD y esta dependencia se agregaria asi
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload,
    # request, tokenpayload)

    data = []

    for db in dbs:
        result = await UnidadEjecutoraService(db).create_unidad(
            payload, request, tokenpayload
        )
        data.append(result)

    return {"data": data[0]}


# endpoint de show o ver registro
@router.get("/{unidad_id}")
async def get_show(unidad_id: int, db: Session = Depends(lambda: next(get_session(0)))):
    return await UnidadEjecutoraService(db).show(unidad_id)


# endpoin para actualizar un registro x
@router.put("/{unidad_id}")
async def update_unidades(
    request: Request,
    unidad_id: int,
    payload: UnidadEjecutoraUpdate,
    # de esta manera llamo todas las bases de datos existentes
    dbs: list[Session] = Depends(lambda: next(get_session())),
    tokenpayload: dict = Depends(verify_jwt_token),
):

    # crear registrro con uan BD y esta dependencia se agregaria asi
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload,
    # request, tokenpayload)

    data = []

    for db in dbs:
        result = await UnidadEjecutoraService(db).update_unidad(
            unidad_id, payload, request, tokenpayload
        )
        data.append(result)

    return {"data": data[0]}


# endpoint para eliminar un registro logicamente
@router.delete("/{unidad_id}")
async def delete_unidades(
    request: Request,
    unidad_id: int,
    # de esta manera llamo todas las bases de datos existentes
    dbs: list[Session] = Depends(lambda: next(get_session())),
    tokenpayload: dict = Depends(verify_jwt_token),
):

    data = []
    for db in dbs:
        result = await UnidadEjecutoraService(db).delete_unidad(
            unidad_id, request, tokenpayload
        )
        data.append(result)

    return {"data": data[0]}
