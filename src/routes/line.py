"""
Endpoints de API para análisis de líneas
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.config import (get_db, get_dbs)
from src.models.schemas import LineCoordinates, APIResponse
from src.services.line_service import line_service
from src.utils.jwt_validator_util import verify_jwt_token

router = APIRouter(prefix="/api/line", tags=["Line Analysis"])


@router.post("/analyze", response_model=APIResponse)
async def analyze_line(
    line_data: LineCoordinates,
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    """
    Analiza una línea y retorna los municipios y departamentos por donde pasa
    
    **Body esperado:**
    ```json
    {
        "type": "line",
        "coordinates": [
            [-74.0817, 4.6097],
            [-74.0517, 4.5797],
            [-74.0217, 4.5497]
        ]
    }
    ```
    
    **Respuesta:**
    - `success`: Indica si la operación fue exitosa
    - `data`: Objeto con el análisis completo
      - `coordenadas_linea`: Coordenadas de la línea analizada
      - `longitud_km`: Longitud total de la línea en km
      - `resumen`: Resumen con totales y longitud
      - `departamentos`: Lista de departamentos por donde pasa (con orden)
      - `municipios`: Lista de municipios por donde pasa (con orden)
    """
    try:
        # Validar que haya coordenadas
        if not line_data.coordinates or len(line_data.coordinates) < 2:
            raise HTTPException(
                status_code=400,
                detail="Se requieren al menos 2 puntos para formar una línea"
            )
        
        # Realizar análisis
        result = line_service.analyze_line(line_data.coordinates, db)
        
        return APIResponse(
            success=True,
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e)
        )

