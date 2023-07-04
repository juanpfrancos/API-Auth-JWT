from fastapi import FastAPI
from routers import users, login, checktoken, signup

app = FastAPI()
app.include_router(users.router)
app.include_router(signup.router)
app.include_router(login.router)
app.include_router(checktoken.router)

# Swagger: http://127.0.0.1:8000/docs
# Redocly: http://127.0.0.1:8000/redoc