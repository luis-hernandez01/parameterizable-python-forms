"""
Servicio para análisis de puntos (Point/Marker)
"""
import json
import os
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from shapely.geometry import Point, shape
from shapely.ops import transform
import pyproj
from src.models.divipola import DepartamentoAika, MunicipioAika
from src.config.config import DATA_DIR, MUNICIPIOS_GEOJSON, DEPARTAMENTOS_GEOJSON

class PointService:
    """Servicio para analizar puntos y determinar en qué municipio/departamento se encuentra"""
    
    def __init__(self):
        # Cargar GeoJSON de municipios y departamentos
        self.municipios_geojson =  self._load_geojson(os.path.join(DATA_DIR, MUNICIPIOS_GEOJSON))
        self.departamentos_geojson = self._load_geojson(os.path.join(DATA_DIR, DEPARTAMENTOS_GEOJSON))
    
    def _load_geojson(self, filepath: str) -> dict:
        """Carga un archivo GeoJSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando {filepath}: {e}")
            return {"type": "FeatureCollection", "features": []}
    
    def _calculate_distance_km(self, point1: Point, point2: Point) -> float:
        """Calcula la distancia entre dos puntos en kilómetros"""
        try:
            # Proyección WGS84 a metros
            wgs84 = pyproj.CRS('EPSG:4326')
            utm = pyproj.CRS('EPSG:3116')  # MAGNA-SIRGAS / Colombia Bogota zone
            
            project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
            point1_projected = transform(project, point1)
            point2_projected = transform(project, point2)
            
            # Distancia en metros, convertir a km
            return point1_projected.distance(point2_projected) / 1000.0
        except:
            # Fallback: aproximación simple
            return point1.distance(point2) * 111.0  # Aproximación: 1 grado ≈ 111 km
    
    def analyze_point(self, coordinates: List[float], db: Session) -> Dict[str, Any]:
        """
        Analiza un punto y determina en qué municipio y departamento se encuentra
        
        Args:
            coordinates: Coordenadas [lng, lat]
            db: Sesión de base de datos
            
        Returns:
            Diccionario con el análisis completo
        """
        try:
            # Crear geometría de punto
            point = Point(coordinates)
            
            # Buscar municipio que contiene el punto
            municipio_encontrado = None
            
            for feature in self.municipios_geojson.get('features', []):
                try:
                    municipio_geom = shape(feature['geometry'])
                    
                    # Verificar si el punto está dentro del municipio
                    if municipio_geom.contains(point):
                        props = feature['properties']
                        codigo_mpio = str(props.get('DPTO')) + str(props.get('MPIO'))
                        
                        if codigo_mpio:
                            # Buscar en BD
                            municipio_db = db.query(MunicipioAika).filter(
                                MunicipioAika.codigo_municipio == codigo_mpio
                            ).first()
                            
                            if municipio_db:
                                # Buscar departamento
                                departamento_db = db.query(DepartamentoAika).filter(
                                    DepartamentoAika.codigo == municipio_db.codigo_departamento
                                ).first()
                                
                                # Calcular distancia al centroide del municipio
                                if municipio_db.latitud and municipio_db.longitud:
                                    centroide = Point(float(municipio_db.longitud), float(municipio_db.latitud))
                                    distancia_km = self._calculate_distance_km(point, centroide)
                                else:
                                    distancia_km = 0.0
                                
                                municipio_encontrado = {
                                    'municipio_id': municipio_db.id,
                                    'codigo_municipio': municipio_db.codigo_municipio,
                                    'nombre_municipio': municipio_db.nombre_municipio,
                                    'departamento_id': departamento_db.id if departamento_db else 0,
                                    'codigo_departamento': municipio_db.codigo_departamento,
                                    'nombre_departamento': departamento_db.nombre if departamento_db else 'N/A',
                                    'distancia_centroide_km': round(distancia_km, 2)
                                }
                                break
                except Exception as e:
                    continue
            
            # Si no se encontró municipio, buscar el más cercano
            if not municipio_encontrado:
                municipio_encontrado = self._find_nearest_municipality(point, db)
            
            # Construir respuesta
            return {
                'tipo': 'marker',
                'coordenadas_punto': coordinates,
                'ubicacion': municipio_encontrado
            }
            
        except Exception as e:
            raise Exception(f"Error al analizar punto: {str(e)}")
    
    def _find_nearest_municipality(self, point: Point, db: Session) -> Dict[str, Any]:
        """Encuentra el municipio más cercano al punto"""
        try:
            # Obtener todos los municipios con coordenadas
            municipios = db.query(MunicipioAika).filter(
                MunicipioAika.latitud.isnot(None),
                MunicipioAika.longitud.isnot(None)
            ).all()
            
            min_distance = float('inf')
            nearest_municipio = None
            
            for municipio in municipios:
                centroide = Point(float(municipio.longitud), float(municipio.latitud))
                distance = self._calculate_distance_km(point, centroide)
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_municipio = municipio
            
            if nearest_municipio:
                # Buscar departamento
                departamento_db = db.query(DepartamentoAika).filter(
                    DepartamentoAika.codigo == nearest_municipio.codigo_departamento
                ).first()
                
                return {
                    'municipio_id': nearest_municipio.id,
                    'codigo_municipio': nearest_municipio.codigo_municipio,
                    'nombre_municipio': f"{nearest_municipio.nombre_municipio} (más cercano)",
                    'departamento_id': departamento_db.id if departamento_db else 0,
                    'codigo_departamento': nearest_municipio.codigo_departamento,
                    'nombre_departamento': departamento_db.nombre if departamento_db else 'N/A',
                    'distancia_centroide_km': round(min_distance, 2)
                }
            else:
                # Fallback si no se encuentra nada
                return {
                    'municipio_id': 0,
                    'codigo_municipio': 'N/A',
                    'nombre_municipio': 'No encontrado',
                    'departamento_id': 0,
                    'codigo_departamento': 'N/A',
                    'nombre_departamento': 'No encontrado',
                    'distancia_centroide_km': 0.0
                }
        except Exception as e:
            raise Exception(f"Error buscando municipio más cercano: {str(e)}")


# Instancia global del servicio
point_service = PointService()

