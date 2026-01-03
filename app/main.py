from fastapi import FastAPI
from app.config.settings import settings
from app.middleware.security import SecurityMiddleware
from app.middleware.error_handler import error_handler

app = FastAPI(
    title=settings.APP_NAME,
    docs_url=None if settings.ENV == "prod" else "/docs",
    redoc_url=None if settings.ENV == "prod" else "/redoc",
)

app.add_middleware(SecurityMiddleware)
app.middleware("http")(error_handler)

@app.get("/boom")
async def boom():
    raise RuntimeError("This should never leak")

@app.get("/health")
async def health():
    return {"status": "ok"}

from app.routers import health, service

app.include_router(health.router)
app.include_router(service.router)



