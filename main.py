# dependencias usadas para este archivo raiz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from src.config.config import Base, engine

# directorios de rutas
from src.routes import (
    categorizacion_route,
    clasificaciones_proyecto_route,
    departamento_route,
    direccion_territorial_route,
    funcionalidades_carreteras_route,
    modo_route,
    municipio_route,
    profesion_route,
    rutas_viales_route,
    tipos_proyectos_route,
    tramo_route,
    unidad_ejecutora_route,
    migrador_route,
    proyecto_route,
    contratos_route
)

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
    allow_methods=["*"
    ],  # se le esta dando permisos a todos los metodos existentes
    allow_headers=["*"],  # Headers personalizados permitidos
)

# registrando mis rutas existentes de las difrentes APIs
# Aquí se incluyen las rutas definidas en la carpeta 'routes'.

app.include_router(migrador_route.router, prefix="/migrar", tags=["Migrar"])



app.include_router(
    municipio_route.router,
    prefix="/municipio",
    tags=["Municipios"],
)

app.include_router(
    departamento_route.router,
    prefix="/departamento",
    tags=["Departamentos"],
)

app.include_router(
    profesion_route.router,
    prefix="/profesion",
    tags=["Profesion"],
)

app.include_router(
    direccion_territorial_route.router,
    prefix="/direccion_territorial",
    tags=["Direccion territorial"],
)
app.include_router(
    tipos_proyectos_route.router, prefix="/tipos_proyectos", tags=["Tipos de proyectos"]
)

app.include_router(tramo_route.router, prefix="/tramos", tags=["Tramos"])
app.include_router(
    categorizacion_route.router, prefix="/categorizacion", tags=["Categorización"]
)
app.include_router(
    rutas_viales_route.router, prefix="/rutas_viales", tags=["Rutas viales"]
)

app.include_router(
    unidad_ejecutora_route.router, prefix="/unidad_ejecutora", tags=["Unidad ejecutora"]
)
app.include_router(
    clasificaciones_proyecto_route.router,
    prefix="/clasificaciones_proyecto",
    tags=["Clasificacion proyectos"],
)
app.include_router(
    funcionalidades_carreteras_route.router,
    prefix="/funcionalidades_carreteras",
    tags=["Funcionalidades carretera"],
)
app.include_router(modo_route.router, prefix="/modo", tags=["Modo"])

app.include_router(
    proyecto_route.router,
    prefix="/proyecto",
    tags=["Proyecto"],
)

app.include_router(
    contratos_route.router,
    prefix="/contratos",
    tags=["Contratos"],
)


#  Documentación con Swagger/OpenAPI
app.mount("/", get_scalar_api_reference())
