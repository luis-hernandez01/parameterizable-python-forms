from datetime import datetime

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from src.config.config import ALGORITHM, SECRET_KEY

# Esquema de seguridad para leer el token del header "Authorization: Bearer <token>"
security = HTTPBearer()


def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifica el token JWT y retorna su payload si es válido.
    """
    token = credentials.credentials
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        exp = payload.get("exp")
        # Validar expiración
        if datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
            )

        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
        )


# sin funcionalidad aun
def require_permission(required_permission: str):
    def _checker(request: Request):
        payload = getattr(request.state, "token_payload", None)
        if not payload or not isinstance(payload, dict):
            raise HTTPException(status_code=401, detail="No autenticado")
        perms = payload.get("permissions")
        if not perms or required_permission not in perms:
            raise HTTPException(status_code=403, detail="Permiso insuficiente")

    return _checker
