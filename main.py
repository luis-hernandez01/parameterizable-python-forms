# dependencias usadas para este archivo raiz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

# directorios de rutas 
from src.routes import unidad_ejecutora_route
from src.config.config import Base, engine

# # --- Crear tablas en todas las bases parametrizadas ---
for engines in engine:
    Base.metadata.create_all(bind=engines)


# Inicialización de la aplicación FastAPI
app = FastAPI(title="Servicios parametrizables", version="1.0.0")
# configuracion de CORS
# permite que aplicaciones externas (por ejemplo,
# un frontend en Angular o React)
# puedan comunicarse con esta API.
# CORS: ajusta a tus orígenes reales
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # Tdos los servicios que envien una peticion tendran permisos
    allow_credentials=True,  # Permitir envío de cookies/autenticación
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
    ],  # se le esta dando permisos a todos los metodos existentes
    allow_headers=["*"],  # Headers personalizados permitidos
)

# registrando mis rutas existentes de las difrentes APIs
# Aquí se incluyen las rutas definidas en la carpeta 'routes'.
app.include_router(unidad_ejecutora_route.router, prefix="/unidad_ejecutora", tags=["Unidad ejecutora"])


#  Documentación con Swagger/OpenAPI
app.mount("/", get_scalar_api_reference())