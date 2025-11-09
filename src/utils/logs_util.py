from fastapi import HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session

from src.models.logs_model import (LogsAika, LogsWayra, TipoOperacionEnum)
from src.schemas.logs_schema import LogCreate


class ILogsUtil:
    def registrar_log(self, data: LogCreate): ...


class LogUtil(ILogsUtil):
    def __init__(self, db: Session):
        self.db = db


def registrar_log(
    self,
    tabla_afectada: str,
    id_registro_afectado: int,
    tipo_operacion: TipoOperacionEnum,
    datos_viejos: dict,
    datos_nuevos: dict,
    id_persona_operacion: int,
    ip_origen: str,
    user_agent: str,
):
    modelos = [LogsAika, LogsWayra]
    resultados = []
    for modelo, db in zip(modelos, self.db):
        try:
            entity = modelo(
                    tabla_afectada=tabla_afectada,
                    id_registro_afectado=id_registro_afectado,
                    tipo_operacion=tipo_operacion,
                    datos_viejos=datos_viejos,
                    datos_nuevos=datos_nuevos,
                    timestamp_operacion=datetime.utcnow(),
                    id_persona_operacion=id_persona_operacion,
                    ip_origen=ip_origen,
                    user_agent=user_agent,
                )
            db.add(entity)
            db.commit()
            db.refresh(entity)
            # return entity
            resultados.append(entity)
        except Exception as e:
                db.rollback()
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando en {modelo.__table__.schema}: {e}")
    return resultados
