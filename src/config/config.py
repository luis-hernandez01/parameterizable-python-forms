import os
from typing import Generator, List, Union

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Cargar variables de entorno
load_dotenv()

# VARIABLES AIKA
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


API_KEY_ = os.getenv("API_KEY_")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
HIDE_TES = os.getenv("ENVIRONMENT")

# Rutas de datos
DATA_DIR: str = "data"
MUNICIPIOS_GEOJSON: str = "municipios_colombia.geojson"
DEPARTAMENTOS_GEOJSON: str = "departamentos_colombia.geojson"

# en produccion se debe de colocar en False para que no genere problemas
DEBUG: bool = False

# SCHEMAS DIFERENTES DENTRO DE LA MISMA BASE
SCHEMA_NAMES = ["Aika", "Wayra"]



# # --- Configura las URLs dinámicamente ---
DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


# # --- Crear engines y sesiones dinámicamente ---

ENGINE_OPTIONS = dict(
    echo=False,
        future=True,
        pool_size=50,          # antes 5
        max_overflow=50,       # antes 10
        pool_timeout=60,       # tiempo máximo antes de dar timeout
        pool_recycle=1800,     # evita conexiones muertas
        pool_pre_ping=True
)

engine = [
    create_engine(DB_URL, **ENGINE_OPTIONS)
    for _ in SCHEMA_NAMES
]

sessions = [
    sessionmaker(bind=e, autocommit=False, autoflush=False)
    for e in engine
]

Base = [
    declarative_base(metadata=MetaData(schema=schema))
    for schema in SCHEMA_NAMES
]

def reset_all_pools():
    for i, schema in enumerate(SCHEMA_NAMES):
        engine[i].pool.dispose()
        # print(f"🔄 Pool reseteado para schema: {schema}")




def get_session(
    db_index: int | None = None,
) -> Generator[Union[Session, List[Session]], None, None]:

    if db_index is not None:
        db = sessions[db_index]()
        try:
            yield db
        finally:
            db.close()

    else:
        dbs = [session_factory() for session_factory in sessions]
        try:
            yield dbs
        finally:
            for db in dbs:
                db.close()




def get_db():
    # Solo la base de datos índice 0
    yield from get_session(0)

def get_dbs():
    # Todas las bases de datos
    yield from get_session()