from fastapi import APIRouter, status
from bson import ObjectId
from models.user import User
from schemas.user import user_schema, users_schema
from config import db_client

router = APIRouter(prefix="/users",
   tags=["Users"],
   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.put("/", response_model=User)
async def user(user: User):
    try:
        user_dict = dict(user)
        del user_dict["id"]
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
        return search_user("_id", ObjectId(user.id))
    except Exception as e:
        return {"error": str(e)}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    try:
        found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
        if not found:
            return {"error": "User not deleted"}
    except Exception as e:
            return {"error": str(e)}

def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except Exception as e:
        return {"error": f"User not found {str(e)}"}