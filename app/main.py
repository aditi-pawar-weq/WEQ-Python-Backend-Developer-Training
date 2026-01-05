from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.middleware.security import SecurityMiddleware
from app.middleware.error_handler import error_handler

from app.db.database import engine, Base
from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables at startup (same behavior as previous startup event)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Ensure new columns added to `users` table when running against an
        # existing SQLite DB created before the `email`/`name` columns were
        # introduced. SQLite's limited ALTER support means `create_all` won't
        # add columns to existing tables, so do a best-effort ALTER here for dev
        # environments. For production use a proper migration (Alembic).

        def _ensure_user_columns(sync_conn):
            try:
                res = sync_conn.execute(text("PRAGMA table_info('users')"))
                existing = {row[1] for row in res.fetchall()}
                if 'email' not in existing:
                    sync_conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR"))
                if 'name' not in existing:
                    sync_conn.execute(text("ALTER TABLE users ADD COLUMN name VARCHAR"))
            except Exception:
                # If anything goes wrong, avoid failing startup — migrations
                # should be handled explicitly in production.
                pass

        await conn.run_sync(_ensure_user_columns)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    docs_url=None if settings.ENV == "prod" else "/docs",
    redoc_url=None if settings.ENV == "prod" else "/redoc",
    lifespan=lifespan,
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
from app.routers import note, protected, auth

app.include_router(protected.router)
app.include_router(auth.router)

app.include_router(note.router)




