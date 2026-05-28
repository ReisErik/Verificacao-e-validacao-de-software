from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import Session, init_db
from contextlib import asynccontextmanager
from app.routes.user_route import router as user_router
from app.routes.auth_route import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {
        "status": "success",
    }