import os
from typing import Generator, List, Union

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Cargar variables de entorno
load_dotenv()

# VARIABLES AIKA
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# VARIABLES WAYRA
POSTGRES_HOST1 = os.getenv("POSTGRES_HOST1", "localhost")
POSTGRES_PORT1 = os.getenv("POSTGRES_PORT1", "5432")
POSTGRES_DB1 = os.getenv("POSTGRES_DB1")
POSTGRES_USER1 = os.getenv("POSTGRES_USER1")
POSTGRES_PASSWORD1 = os.getenv("POSTGRES_PASSWORD1")


API_KEY_ = os.getenv("API_KEY_")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# # --- Configura las URLs dinámicamente ---
DB_CONFIGS = [
    f"postgresql+psycopg2://notifications:ka8z53PkKZE5uNmCAOyVA2nMbiHNpWE3"
    f"@dpg-d3d8c3jipnbc73fck58g-a.frankfurt-postgres.render.com/notifications_si78",
    f"postgresql+psycopg2://root:9vUcmw7EWU4W3fdqfaK4nZ7ggtJ22Bu7"
    f"@dpg-d3ogh1ili9vc73c52m3g-a.oregon-postgres.render.com/wayra",
    # f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    # f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
    # f"postgresql+psycopg2://{POSTGRES_USER1}:{POSTGRES_PASSWORD1}"
    # f"@{POSTGRES_HOST1}:{POSTGRES_PORT1}/{POSTGRES_DB1}",
]

# # --- Crear engines y sesiones dinámicamente ---
engine = [create_engine(url, echo=False, future=True) for url in DB_CONFIGS]
sessions = [sessionmaker(autocommit=False, autoflush=False, bind=e) for e in engine]

# # --- Base única para todos los modelos ---
Base = declarative_base()


def get_session(
    db_index: int | None = None,
) -> Generator[Union[Session, List[Session]], None, None]:
    """
    Devuelve:
      - Una sola sesión (si se pasa db_index)
      - Una lista de sesiones (si no se pasa)
    """
    # Caso 1 → sesión única
    if db_index is not None:
        db = sessions[db_index]()
        try:
            yield db
        finally:
            db.close()
    else:
        # Caso 2 → lista de sesiones
        dbs = [Session() for Session in sessions]
        try:
            yield dbs
        finally:
            for db in dbs:
                db.close()
