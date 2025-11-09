"""
Servicio para análisis de líneas (LineString)
"""
import json
import os
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from shapely.geometry import LineString, shape
from shapely.ops import transform
import pyproj
from src.models.divipola import DepartamentoAika as Departamento, MunicipioAika as Municipio
from src.config.config import DATA_DIR, MUNICIPIOS_GEOJSON, DEPARTAMENTOS_GEOJSON

class LineService:
    """Servicio para analizar líneas y determinar por qué municipios/departamentos pasa"""
    
    def __init__(self):
        # Cargar GeoJSON de municipios y departamentos
        self.municipios_geojson =  self._load_geojson(os.path.join(DATA_DIR, MUNICIPIOS_GEOJSON))
        self.departamentos_geojson = self._load_geojson(os.path.join(DATA_DIR, DEPARTAMENTOS_GEOJSON))
        
        # print(f"[DEBUG] Municipios cargados: {len(self.municipios_geojson.get('features', []))}")
        # print(f"[DEBUG] Departamentos cargados: {len(self.departamentos_geojson.get('features', []))}")

    def _load_geojson(self, filepath: str) -> dict:
        """Carga un archivo GeoJSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando {filepath}: {e}")
            return {"type": "FeatureCollection", "features": []}
    
    def _calculate_line_length_km(self, line: LineString) -> float:
        """Calcula la longitud de una línea en kilómetros"""
        try:
            # Proyección WGS84 a metros (usar proyección apropiada para Colombia)
            wgs84 = pyproj.CRS('EPSG:4326')
            utm = pyproj.CRS('EPSG:3116')  # MAGNA-SIRGAS / Colombia Bogota zone
            
            project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
            line_projected = transform(project, line)
            
            # Longitud en metros, convertir a km
            return line_projected.length / 1000.0
        except:
            # Fallback: aproximación simple
            return line.length * 111.0  # Aproximación: 1 grado ≈ 111 km
    
    def analyze_line(self, coordinates: List[List[float]], db: Session) -> Dict[str, Any]:
        """
        Analiza una línea y determina por qué municipios y departamentos pasa
        
        Args:
            coordinates: Lista de coordenadas [[lng, lat], ...]
            db: Sesión de base de datos
            
        Returns:
            Diccionario con el análisis completo
        """
        try:
            # Crear geometría de línea
            line = LineString(coordinates)
            
            # Calcular longitud
            longitud_km = self._calculate_line_length_km(line)
            
            # Buscar municipios por donde pasa la línea
            municipios_encontrados = []
            municipios_ids = set()
            
            for feature in self.municipios_geojson.get('features', []):
                try:
                    municipio_geom = shape(feature['geometry'])
                    
                    # Verificar si la línea intersecta con el municipio
                    if line.intersects(municipio_geom):
                        props = feature['properties']
                        codigo_mpio = str(props.get('DPTO')) + str(props.get('MPIO'))
                        
                        if codigo_mpio and codigo_mpio not in municipios_ids:
                            municipios_ids.add(codigo_mpio)
                            
                            # Buscar en BD
                            municipio_db = db.query(Municipio).filter(
                                Municipio.codigo_municipio == codigo_mpio
                            ).first()
                            
                            if municipio_db:
                                # Buscar departamento
                                departamento_db = db.query(Departamento).filter(
                                    Departamento.codigo == municipio_db.codigo_departamento
                                ).first()
                                
                                municipios_encontrados.append({
                                    'id': municipio_db.id,
                                    'codigo_municipio': municipio_db.codigo_municipio,
                                    'nombre_municipio': municipio_db.nombre_municipio,
                                    'codigo_departamento': municipio_db.codigo_departamento,
                                    'nombre_departamento': departamento_db.nombre if departamento_db else 'N/A',
                                    'orden': len(municipios_encontrados) + 1
                                })
                except Exception as e:
                    continue
            
            # Buscar departamentos por donde pasa la línea
            departamentos_encontrados = []
            departamentos_ids = set()
            
            for feature in self.departamentos_geojson.get('features', []):
                try:
                    depto_geom = shape(feature['geometry'])
                    
                    # Verificar si la línea intersecta con el departamento
                    if line.intersects(depto_geom):
                        props = feature['properties']
                        codigo_depto = props.get('DPTO') or props.get('DPTO')
                        
                        if codigo_depto and codigo_depto not in departamentos_ids:
                            departamentos_ids.add(codigo_depto)
                            
                            # Buscar en BD
                            depto_db = db.query(Departamento).filter(
                                Departamento.codigo == codigo_depto
                            ).first()
                            
                            if depto_db:
                                departamentos_encontrados.append({
                                    'id': depto_db.id,
                                    'codigo_departamento': depto_db.codigo,
                                    'nombre_departamento': depto_db.nombre,
                                    'orden': len(departamentos_encontrados) + 1
                                })
                except Exception as e:
                    continue
            
            # Construir respuesta
            return {
                'tipo': 'line',
                'coordenadas_linea': coordinates,
                'longitud_km': round(longitud_km, 2),
                'resumen': {
                    'total_departamentos': len(departamentos_encontrados),
                    'total_municipios': len(municipios_encontrados),
                    'longitud_km': round(longitud_km, 2)
                },
                'departamentos': departamentos_encontrados,
                'municipios': municipios_encontrados
            }
            
        except Exception as e:
            raise Exception(f"Error al analizar línea: {str(e)}")


# Instancia global del servicio
line_service = LineService()

