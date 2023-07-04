from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta
from models.user import User
from schemas.user import user_schema
from config import db_client, crypt_context, JWT_SECRET, JWT_ALGORITHM

ACCESS_TOKEN_DURATION = 4

router = APIRouter(prefix="/login",
                   tags=["login"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})



def search_user(username: str):
    user_db = db_client.users.find_one({"username": username})
    if not user_db:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist")
    user = User(**user_schema(user_db))
    return user

@router.post("/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="wrong user")
    if not crypt_context.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="wrong password")

    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, JWT_SECRET, algorithm=JWT_ALGORITHM), "token_type": "bearer"}