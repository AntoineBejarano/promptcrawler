"""
FastAPI main application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import jobs, auth, users
from app.config import settings

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PromptCrawler API",
    description="API para convertir prompts en datasets estructurados",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])


@app.get("/")
async def root():
    return {"message": "PromptCrawler API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

