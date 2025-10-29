from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union, Any
import importlib
import pandas as pd
import io
from datetime import datetime
from src.config.config import get_session
from src.utils.jwt_validator_util import verify_jwt_token
router = APIRouter()



# Helpers

def parse_datetime(value: Any):
    """Convierte cadenas o números en datetime válido o None."""
    if pd.isna(value) or value in ("", None):
        return None
    if isinstance(value, datetime):
        return value
    try:
        return pd.to_datetime(value)
    except Exception:
        return None


# Endpoint principal

@router.post("/upload-excel")
async def upload_excel(
    file: UploadFile = File(...),
    modelo: str = Form(...),   # Ej: "unidad_ejecutora"
    clases: str = Form(...),   # Ej: "UnidadEjecutora"
    dbs: Union[Session, List[Session]] = Depends(get_session),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    """
    Servicio dinámico para subir un Excel y poblar tablas según el modelo.
    Compatible con una o múltiples bases de datos según get_session().
    """
    try:
        # Leer Excel desde memoria
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        # Limpiar columnas y valores nulos
        df.columns = df.columns.str.strip()
        df = df.where(pd.notnull(df), None)

        # Cargar modelo dinámicamente
        module_name = f"src.models.{modelo}_model"
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise HTTPException(status_code=400, detail=f"No se encontró el módulo '{module_name}'")

        try:
            model_class = getattr(module, clases)
        except AttributeError:
            raise HTTPException(status_code=400, detail=f"No se encontró la clase '{clases}' en {module_name}")

        # Validar columnas coincidentes
        model_columns = set(model_class.__table__.columns.keys())
        df_filtered = df[[c for c in df.columns if c in model_columns]]

        if df_filtered.empty:
            raise HTTPException(status_code=400, detail="Ninguna columna del Excel coincide con el modelo")

        # Parsear fechas automáticamente
        for col in df_filtered.columns:
            if any(x in col.lower() for x in ["fecha", "created", "updated", "deleted", "time", "at"]):
                df_filtered[col] = df_filtered[col].apply(parse_datetime)

        # Asegurar que siempre sea una lista de sesiones
        db_list = dbs if isinstance(dbs, list) else [dbs]

        registros_creados = 0

        for db in db_list:
            try:
                for _, row in df_filtered.iterrows():
                    data = row.to_dict()

                    # Asignar valores por defecto comunes
                    # if "created_at" in model_columns and not data.get("created_at"):
                    data["created_at"] = datetime.now()
                    data["updated_at"] = None
                    data["deleted_at"] = None
                    data["id_persona"] = 2
                    # if "activo" in model_columns and not data.get("activo"):
                    data["activo"] = True 

                    instance = model_class(**data)
                    db.add(instance)
                    registros_creados += 1

                db.commit()

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Error al insertar en una base: {e}")

        return {
            "success": True,
            "modelo": modelo,
            "registros_insertados": registros_creados,
            "bases_actualizadas": len(db_list)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
