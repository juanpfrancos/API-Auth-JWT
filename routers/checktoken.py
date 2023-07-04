from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from models.user import User
from schemas.user import user_schema
from config import db_client, JWT_SECRET, JWT_ALGORITHM


ACCESS_TOKEN_DURATION = 4


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(prefix="/check",
                   tags=["check"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})



def search_user(username: str):
    user = User(**user_schema(db_client.users.find_one({"username": username})))
    return user


async def auth_user(token: str = Depends(oauth2_scheme)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


