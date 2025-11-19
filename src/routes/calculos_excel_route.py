from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import os
from pathlib import Path
from src.services.processor import process_all

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()


@router.post("/procesar")
async def procesar_archivos(
    emisiones4: UploadFile = File(..., description="CSV con columnas PR_INICIAL, PR_FINAL, Trimestral, codigo_via, ID (opcional)") ,
    emisiones_trimestre: UploadFile = File(..., description="CSV con columnas Trimestral, Emisiones, ID (opcional)")
):
    try:
        # leer en memoria (los UploadFile ya proveen file-like)
        # nos aseguramos de posicionar al inicio
        emisiones4.file.seek(0)
        emisiones_trimestre.file.seek(0)

        df1 = pd.read_csv(emisiones4.file, sep=';', decimal=',')
        df2 = pd.read_csv(emisiones_trimestre.file, sep=';', decimal=',')

        # Validaciones básicas de columnas
        required_cols_1 = {"PR_INICIAL", "PR_FINAL", "Trimestral", "codigo_via"}
        required_cols_2 = {"Trimestral", "Emisiones"}

        if not required_cols_1.issubset(set(df1.columns)):
            missing = required_cols_1 - set(df1.columns)
            raise HTTPException(status_code=400, detail=f"Faltan columnas en emisiones4.csv: {missing}")

        if not required_cols_2.issubset(set(df2.columns)):
            missing = required_cols_2 - set(df2.columns)
            raise HTTPException(status_code=400, detail=f"Faltan columnas en emisiones_trimestre.csv: {missing}")

        # Procesar todo
        result, short_result = process_all(df1, df2)

        # Guardar salidas
        result_path = OUTPUT_DIR / "result.csv"
        short_path = OUTPUT_DIR / "short_result.csv"

        result.to_csv(result_path, index=False)
        short_result.to_csv(short_path, index=False, sep=';', decimal=',')

        return {
            "message": "Procesamiento completado",
            "download_result": "/download/result",
            "download_short": "/download/short",
            "rows_result": len(result),
            "rows_short": len(short_result)
        }

    except HTTPException:
        raise
    except Exception as e:
        # devolver traza limitada para debug
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/result")
def download_result():
    path = OUTPUT_DIR / "result.csv"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Archivo result.csv no encontrado. Ejecuta /procesar primero.")
    return FileResponse(path, filename="result.csv")


@router.get("/download/short")
def download_short():
    path = OUTPUT_DIR / "short_result.csv"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Archivo short_result.csv no encontrado. Ejecuta /procesar primero.")
    return FileResponse(path, filename="short_result.csv")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("router.main:router", host="0.0.0.0", port=8000, reload=True)