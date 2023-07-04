from pymongo import MongoClient
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

CNN_STRING = os.getenv("CNN_STRING")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


db_client = MongoClient(CNN_STRING).users
crypt_context = CryptContext(schemes=["bcrypt"])