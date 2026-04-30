import os
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from src.config.database import Base, engine
from src import models  # noqa: F401  ensure models register with Base
from src.handlers.custom_exceptions import APIKeyException
from src.handlers.exception_handler import (
    validation_exception_handler, general_exception_handler, api_key_exception_handler)

from src.routes import todos

load_dotenv()

DEBUG = bool(int(os.getenv("DEBUG", 1)))


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FastAPI Backend",
    description="This is FastAPI Backend API Documentation",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,  # Disable Swagger UI
    redoc_url="/redoc" if DEBUG else None,  # Disable ReDoc
    openapi_url="/openapi.json" if DEBUG else None,  # Disable OpenAPI
    lifespan=lifespan,
)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(APIKeyException, api_key_exception_handler)


# Include routes
app.include_router(todos.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": 200, "message": "Server is up and running!", "data": "Made with ❤️"}


@app.get("/health")
async def health_check():
    return {"status": 200, "message": "OK"}
