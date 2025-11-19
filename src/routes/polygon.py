"""
Endpoints de API para análisis de polígonos
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.config import (get_db, get_dbs)
from src.models.schemas import PolygonCoordinates, APIResponse
from src.services.polygon_service import polygon_service
from src.utils.jwt_validator_util import verify_jwt_token
router = APIRouter(prefix="/api/polygon", tags=["Polygon Analysis"])


@router.post("/analyze", response_model=APIResponse)
async def analyze_polygon(
    polygon_data: PolygonCoordinates,
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    """
    Analiza un polígono y retorna los municipios y departamentos que intersecta
    
    **Body esperado:**
    ```json
    {
        "coordinates": [
            [
                [-74.0817, 4.6097],
                [-74.0817, 4.5397],
                [-74.0017, 4.5397],
                [-74.0017, 4.6097],
                [-74.0817, 4.6097]
            ]
        ]
    }
    ```
    
    **Respuesta:**
    - `success`: Indica si la operación fue exitosa
    - `data`: Objeto con el análisis completo
      - `coordenadas_poligono`: Coordenadas del polígono analizado
      - `area_total_km2`: Área total del polígono en km²
      - `resumen`: Resumen con totales
      - `departamentos`: Lista de departamentos intersectados
      - `municipios`: Lista de municipios intersectados
    """
    try:
        # Validar que haya coordenadas
        if not polygon_data.coordinates or len(polygon_data.coordinates) == 0:
            raise HTTPException(
                status_code=400,
                detail="Se requieren coordenadas válidas para el polígono"
            )

        # Validar que el primer anillo tenga al menos 2 puntos
        if len(polygon_data.coordinates[0]) < 2:
            raise HTTPException(
                status_code=400,
                detail="El polígono debe tener al menos 2 puntos"
            )
        
        # Realizar análisis
        result = polygon_service.analyze_polygon(polygon_data.coordinates, db)
        result["tipo"] = polygon_data.type
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

