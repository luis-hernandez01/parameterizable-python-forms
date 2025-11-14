from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from src.services.upload_service import send_file_to_external_service

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    # container: str = Form(...)
):
    """
    Recibe un archivo localmente y lo reenvía al servicio externo.
    """
    try:
        response = await send_file_to_external_service(file)
        return JSONResponse(content=response)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
