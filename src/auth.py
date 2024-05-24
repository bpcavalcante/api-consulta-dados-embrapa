import time
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Dict

# Carregar as chaves
with open("private_key.pem", "r") as f:
    private_key = f.read()

with open("public_key.pem", "r") as f:
    public_key = f.read()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função utilitária para criar um token JWT
def create_jwt_token(data: Dict, expires_in: int = 3600):
    payload = data.copy()
    payload.update({"exp": time.time() + expires_in})
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

# Função utilitária para decodificar um token JWT
def decode_jwt_token(token: str):
    try:
        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirou",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependência para obter o usuário atual
def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_jwt_token(token)
