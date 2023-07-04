from fastapi import APIRouter, HTTPException, status
from models.user import User
from schemas.user import user_schema
from config import db_client, crypt_context


router = APIRouter(prefix="/signup",
   tags=["User"],
   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    try:
        user_dict = dict(user)
        user_dict.update({"password":crypt_context.encrypt(user.password)})
        del user_dict["id"]
        _id = db_client.users.insert_one(user_dict).inserted_id
        new_user = user_schema(db_client.users.find_one({"_id": _id}))
        return User(**new_user)
    except Exception as e:
        return {"error": f"User not created {str(e)}"}


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except Exception as e:
        return {"error": f"User not found {str(e)}"}