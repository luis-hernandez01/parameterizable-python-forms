# from fastapi import APIRouter, Depends, Query, Request
# from sqlalchemy.orm import Session
# from typing import Dict, Any, Optional

# from src.config.config import (get_db, get_dbs)
# from src.services.presenta_services import PresentaService
# from src.schemas.Presenta_schema import (PaginacionSchema, 
#                                                 PresentaCreate,
#                                                 PresentaUpdate)
# from src.utils.jwt_validator_util import verify_jwt_token

# # inicializacion del roter
# router = APIRouter()

# @router.get("/all")
# def list_all(
#     # de esta manera llamo solamente la primera base de datos
#     db: Session = Depends(get_db),
#     tokenpayload: dict = Depends(verify_jwt_token),
# ):
#     return PresentaService(db).all()


# # endpoint de listar data con paginacion incluida
# @router.get("/", response_model=PaginacionSchema)
# def lista(
#     page: int = Query(1, ge=1),
#     per_page: int = Query(50, ge=1, le=200),
#     activo: Optional[bool] = Query(True, description="Filtrar por estado activo (true o false)"),
#     # de esta manera llamo solamente la primera base de datos
#     db: Session = Depends(get_db),
#     tokenpayload: dict = Depends(verify_jwt_token)
# ) -> Dict[str, Any]:
#     skip = (page - 1) * per_page
#     limit = per_page
#     data = PresentaService(db).listar(activo=activo, skip=skip, limit=limit)
#     total = PresentaService(db).count(activo=activo)  
#     # Método adicional para contar todos los datos
#     return {
#         "items": data,
#         "per_page": per_page,
#         "size": limit,
#         "total": total,
#         "last_page" : (total + per_page - 1) // per_page,
#         "page": page,
#         "pages": (total + limit - 1) // limit  # Redondeo hacia arriba
        
#     }
    
#     # endpoin de crear registro
# @router.post("/")
# def creates(request: Request, 
#                         payload: PresentaCreate, 
#                         # de esta manera llamo todas las bases de datos existentes
#                         dbs: list[Session] = Depends(get_dbs),
#                         tokenpayload: dict = Depends(verify_jwt_token)):
#     result = PresentaService(dbs).create(payload, request, tokenpayload)
#     return {"data": result}


# # endpoint de show o ver registro
# @router.get("/{presenta_id}")
# def get_show(presenta_id: int, 
#                 db: Session = Depends(get_db),
#                 tokenpayload: dict = Depends(verify_jwt_token)):
#     return PresentaService(db).show(presenta_id)


# # endpoin para actualizar un registro x
# @router.put("/{presenta_id}")
# def update(request: Request, 
#                         presenta_id: int,
#                         payload: PresentaUpdate,
#                         # de esta manera llamo todas las bases de datos existentes
#                         dbs: list[Session] = Depends(get_dbs),
#                         tokenpayload: dict = Depends(verify_jwt_token)):
#     result = PresentaService(dbs).updates(presenta_id, payload, request, tokenpayload)
#     return {"data": result}


# # endpoint para eliminar un registro logicamente
# @router.delete("/{presenta_id}")
# def delete(request: Request, 
#                         presenta_id: int, 
#                         # de esta manera llamo todas las bases de datos existentes
#                         dbs: list[Session] = Depends(get_dbs),
#                         tokenpayload: dict = Depends(verify_jwt_token)):
#     result = PresentaService(dbs).deletes(presenta_id, request, tokenpayload)
#     return {"data": result}


# @router.post("/{presenta_id}/reactivate")
# def reactivates(request: Request, 
#                         presenta_id: int, 
#                         # de esta manera llamo todas las bases de datos existentes
#                         dbs: list[Session] = Depends(get_dbs),
#                         tokenpayload: dict = Depends(verify_jwt_token)):
#     result = PresentaService(dbs).reactivate(presenta_id, request, tokenpayload)
#     return {"data": result}

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from playwright.sync_api import sync_playwright
from starlette.concurrency import run_in_threadpool

router = APIRouter()

executor = ThreadPoolExecutor(max_workers=2)

def generar_pdf_sync(html: str):
    buffer = BytesIO()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.set_content(html, wait_until="load")

        pdf_bytes = page.pdf(
        format="A4",
        print_background=True,
        display_header_footer=True,
        margin={"top": "60px", "bottom": "60px", "left": "20px", "right": "20px"},
        header_template="""
            <div style="font-size:10px; width:100%; text-align:center; margin-top:10px;">
                <span class="date"></span> — <span class="title"></span>
            </div>
        """,
        footer_template="""
            <div style="font-size:10px; width:100%; text-align:center; margin-bottom:10px;">
                Página <span class="pageNumber"></span> de <span class="totalPages"></span>
            </div>
        """
        )

        buffer.write(pdf_bytes)
        buffer.seek(0)

        browser.close()

    return buffer


@router.post("/html-to-pdf")
async def html_to_pdf(file: UploadFile = File(...)):
    html_content = (await file.read()).decode("utf-8")

    # Ejecutamos Playwright Sync en un hilo aparte
    buffer = await run_in_threadpool(generar_pdf_sync, html_content)

    return StreamingResponse(
        buffer,
        media_type="routerlication/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte.pdf"}
    )
