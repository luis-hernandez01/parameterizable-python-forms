"""
Schemas Pydantic para validación de datos
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Union


# ============================================================================
# SCHEMAS DE ENTRADA
# ============================================================================

class PolygonCoordinates(BaseModel):
    """Coordenadas de polígono en formato GeoJSON"""
    type: str = Field(default="polygon", description="Tipo de geometría")
    coordinates: List[List[List[float]]] = Field(
        ...,
        description="Coordenadas del polígono en formato GeoJSON [[[lng, lat], ...]]"
    )


class LineCoordinates(BaseModel):
    """Coordenadas de línea en formato GeoJSON"""
    type: str = Field(default="line", description="Tipo de geometría")
    coordinates: List[List[float]] = Field(
        ...,
        description="Coordenadas de la línea en formato GeoJSON [[lng, lat], ...]"
    )


class PointCoordinates(BaseModel):
    """Coordenadas de punto en formato GeoJSON"""
    type: str = Field(default="marker", description="Tipo de geometría")
    coordinates: List[float] = Field(
        ...,
        description="Coordenadas del punto en formato GeoJSON [lng, lat]"
    )


# ============================================================================
# SCHEMAS DE RESPUESTA - POLÍGONOS
# ============================================================================

class MunicipioIntersectado(BaseModel):
    """Información de municipio intersectado"""
    id: int
    codigo_municipio: str
    nombre_municipio: str
    codigo_departamento: str
    nombre_departamento: str
    porcentaje_interseccion: float
    area_interseccion_km2: float


class DepartamentoIntersectado(BaseModel):
    """Información de departamento intersectado"""
    id: int
    codigo_departamento: str
    nombre_departamento: str
    porcentaje_interseccion: float
    area_interseccion_km2: float


class AnalisisResumen(BaseModel):
    """Resumen del análisis"""
    total_departamentos: int
    total_municipios: int


class AnalisisPolygonResponse(BaseModel):
    """Respuesta completa del análisis de polígono"""
    tipo: str = "polygon"
    coordenadas_poligono: List[List[List[float]]]
    area_total_km2: float
    resumen: AnalisisResumen
    departamentos: List[DepartamentoIntersectado]
    municipios: List[MunicipioIntersectado]


# ============================================================================
# SCHEMAS DE RESPUESTA - LÍNEAS
# ============================================================================

class MunicipioEnRuta(BaseModel):
    """Información de municipio por donde pasa la línea"""
    id: int
    codigo_municipio: str
    nombre_municipio: str
    codigo_departamento: str
    nombre_departamento: str
    orden: int  # Orden en que aparece en la ruta


class DepartamentoEnRuta(BaseModel):
    """Información de departamento por donde pasa la línea"""
    id: int
    codigo_departamento: str
    nombre_departamento: str
    orden: int  # Orden en que aparece en la ruta


class AnalisisLineaResumen(BaseModel):
    """Resumen del análisis de línea"""
    total_departamentos: int
    total_municipios: int
    longitud_km: float


class AnalisisLineResponse(BaseModel):
    """Respuesta completa del análisis de línea"""
    tipo: str = "line"
    coordenadas_linea: List[List[float]]
    longitud_km: float
    resumen: AnalisisLineaResumen
    departamentos: List[DepartamentoEnRuta]
    municipios: List[MunicipioEnRuta]


# ============================================================================
# SCHEMAS DE RESPUESTA - PUNTOS
# ============================================================================

class UbicacionPunto(BaseModel):
    """Información de ubicación del punto"""
    municipio_id: int
    codigo_municipio: str
    nombre_municipio: str
    departamento_id: int
    codigo_departamento: str
    nombre_departamento: str
    distancia_centroide_km: float  # Distancia al centroide del municipio


class AnalisisPointResponse(BaseModel):
    """Respuesta completa del análisis de punto"""
    tipo: str = "marker"
    coordenadas_punto: List[float]
    ubicacion: UbicacionPunto


# ============================================================================
# SCHEMA DE RESPUESTA GENÉRICA
# ============================================================================

class APIResponse(BaseModel):
    """Respuesta estándar de la API"""
    success: bool
    data: Optional[Union[AnalisisPolygonResponse, AnalisisLineResponse, AnalisisPointResponse, dict]] = None
    error: Optional[str] = None

