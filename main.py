from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, login, checktoken, signup

app = FastAPI(title="Auth - API", description="Developed with ❤ by @Juanpfrancos")

app.include_router(users.router)
app.include_router(signup.router)
app.include_router(login.router)
app.include_router(checktoken.router)

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    'http://127.0.0.1:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)