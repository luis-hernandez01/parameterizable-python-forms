"""
Servicio para análisis de polígonos con datos DIVIPOLA desde MySQL
"""
import json
import os
from typing import List, Dict, Any
from shapely.geometry import shape, Polygon as ShapelyPolygon
from sqlalchemy.orm import Session
from src.models.divipola import DepartamentoAika, MunicipioAika
from src.config.config import DATA_DIR, MUNICIPIOS_GEOJSON, DEPARTAMENTOS_GEOJSON


class PolygonAnalysisService:
    """Servicio para análisis geoespacial de polígonos"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
        self._municipios_geojson = None
        self._departamentos_geojson = None
    
    @property
    def municipios_geojson(self) -> Dict:
        """Carga lazy de datos GeoJSON de municipios"""
        if self._municipios_geojson is None:
            geojson_path = os.path.join(self.data_dir, MUNICIPIOS_GEOJSON)
            with open(geojson_path, 'r', encoding='utf-8') as f:
                self._municipios_geojson = json.load(f)
        return self._municipios_geojson
    
    @property
    def departamentos_geojson(self) -> Dict:
        """Carga lazy de datos GeoJSON de departamentos"""
        if self._departamentos_geojson is None:
            geojson_path = os.path.join(self.data_dir, DEPARTAMENTOS_GEOJSON)
            with open(geojson_path, 'r', encoding='utf-8') as f:
                self._departamentos_geojson = json.load(f)
        return self._departamentos_geojson
    
    def analyze_polygon(self, polygon_coords: List[List[List[float]]], db: Session) -> Dict[str, Any]:
        """
        Analiza un polígono y retorna municipios y departamentos intersectados
        
        Args:
            polygon_coords: Coordenadas del polígono en formato GeoJSON
            db: Sesión de base de datos
        
        Returns:
            Dict con análisis completo
        """
        # Crear polígono Shapely
        user_polygon = ShapelyPolygon(polygon_coords[0])
        
        # Analizar intersecciones
        municipios_result = self._find_intersecting_municipios(user_polygon, db)
        departamentos_result = self._find_intersecting_departamentos(user_polygon, db)
        
        return {
            "coordenadas_poligono": polygon_coords,
            "area_total_km2": round(user_polygon.area * 111 * 111, 2),
            "resumen": {
                "total_departamentos": len(departamentos_result),
                "total_municipios": len(municipios_result)
            },
            "departamentos": departamentos_result,
            "municipios": municipios_result
        }
    
    def _find_intersecting_municipios(self, user_polygon: ShapelyPolygon, db: Session) -> List[Dict]:
        """Encuentra municipios que intersectan con el polígono"""
        municipios_intersectados = []
        
        # Iterar sobre features de municipios en GeoJSON
        for feature in self.municipios_geojson.get('features', []):
            try:
                municipio_geom = shape(feature['geometry'])
                
                if user_polygon.intersects(municipio_geom):
                    props = feature.get('properties', {})
                    cod_mpio = str(props.get('DPTO')) + str(props.get('MPIO'))


                    # Buscar información en MySQL
                    municipio_db = db.query(MunicipioAika).filter(
                        MunicipioAika.codigo_municipio == cod_mpio
                    ).first()
                    
                    if municipio_db:
                        # Calcular intersección
                        intersection = user_polygon.intersection(municipio_geom)
                        porcentaje_area = (intersection.area / municipio_geom.area) * 100
                        
                        # Obtener departamento
                        departamento_db = db.query(DepartamentoAika).filter(
                            DepartamentoAika.codigo == municipio_db.codigo_departamento
                        ).first()
                        
                        municipios_intersectados.append({
                            "id": municipio_db.id,
                            "codigo_municipio": municipio_db.codigo_municipio,
                            "nombre_municipio": municipio_db.nombre_municipio,
                            "codigo_departamento": municipio_db.codigo_departamento,
                            "nombre_departamento": departamento_db.nombre if departamento_db else "",
                            "porcentaje_interseccion": round(porcentaje_area, 2),
                            "area_interseccion_km2": round(intersection.area * 111 * 111, 2)
                        })
            except Exception as e:
                continue
        
        # Ordenar por porcentaje de intersección
        municipios_intersectados.sort(key=lambda x: x['porcentaje_interseccion'], reverse=True)
        return municipios_intersectados
    
    def _find_intersecting_departamentos(self, user_polygon: ShapelyPolygon, db: Session) -> List[Dict]:
        """Encuentra departamentos que intersectan con el polígono"""
        departamentos_intersectados = []
        
        # Iterar sobre features de departamentos en GeoJSON
        for feature in self.departamentos_geojson.get('features', []):
            try:
                depto_geom = shape(feature['geometry'])
                
                if user_polygon.intersects(depto_geom):
                    props = feature.get('properties', {})
                    cod_dpto = props.get('DPTO') or props.get('DPTO')
                    
                    # Buscar información en MySQL
                    depto_db = db.query(DepartamentoAika).filter(
                        DepartamentoAika.codigo == cod_dpto
                    ).first()
                    
                    if depto_db:
                        # Calcular intersección
                        intersection = user_polygon.intersection(depto_geom)
                        porcentaje_area = (intersection.area / depto_geom.area) * 100
                        
                        departamentos_intersectados.append({
                            "id": depto_db.id,
                            "codigo_departamento": depto_db.codigo,
                            "nombre_departamento": depto_db.nombre,
                            "porcentaje_interseccion": round(porcentaje_area, 2),
                            "area_interseccion_km2": round(intersection.area * 111 * 111, 2)
                        })
            except Exception as e:
                continue
        
        # Ordenar por porcentaje de intersección
        departamentos_intersectados.sort(key=lambda x: x['porcentaje_interseccion'], reverse=True)
        return departamentos_intersectados


# Instancia singleton del servicio
polygon_service = PolygonAnalysisService()

