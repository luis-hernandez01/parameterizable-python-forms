"""
Endpoints de API para análisis de puntos
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.config import (get_db, get_dbs)
from src.models.schemas import PointCoordinates, APIResponse
from src.services.point_service import point_service
from src.utils.jwt_validator_util import verify_jwt_token

router = APIRouter(prefix="/api/point", tags=["Point Analysis"])


@router.post("/analyze", response_model=APIResponse)
async def analyze_point(
    point_data: PointCoordinates,
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    """
    Analiza un punto y retorna el municipio y departamento donde se encuentra
    
    **Body esperado:**
    ```json
    {
        "type": "marker",
        "coordinates": [-74.0817, 4.6097]
    }
    ```
    
    **Respuesta:**
    - `success`: Indica si la operación fue exitosa
    - `data`: Objeto con el análisis completo
      - `coordenadas_punto`: Coordenadas del punto analizado [lng, lat]
      - `ubicacion`: Información de ubicación
        - `municipio_id`: ID del municipio
        - `codigo_municipio`: Código DIVIPOLA del municipio
        - `nombre_municipio`: Nombre del municipio
        - `departamento_id`: ID del departamento
        - `codigo_departamento`: Código DIVIPOLA del departamento
        - `nombre_departamento`: Nombre del departamento
        - `distancia_centroide_km`: Distancia al centroide del municipio en km
    """
    try:
        # Validar que haya coordenadas
        if not point_data.coordinates or len(point_data.coordinates) != 2:
            raise HTTPException(
                status_code=400,
                detail="Se requieren exactamente 2 coordenadas [lng, lat] para un punto"
            )
        
        # Validar rangos de coordenadas (Colombia aproximadamente)
        lng, lat = point_data.coordinates
        if not (-79 <= lng <= -66):
            raise HTTPException(
                status_code=400,
                detail=f"Longitud fuera de rango para Colombia: {lng}"
            )
        if not (-4.5 <= lat <= 13.5):
            raise HTTPException(
                status_code=400,
                detail=f"Latitud fuera de rango para Colombia: {lat}"
            )
        
        # Realizar análisis
        result = point_service.analyze_point(point_data.coordinates, db)
        
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

