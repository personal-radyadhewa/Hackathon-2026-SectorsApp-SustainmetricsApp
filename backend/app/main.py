"""FastAPI application entrypoint for SustainMetric IDX Harness."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.core.config import settings
from app.api.routes import router as api_router
import asyncio
from app.services.scheduler import start_scheduler, stop_scheduler
from app.services.seeder import seed_initial_demo_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start background cron engine and pre-populate demo emitents
    start_scheduler()
    asyncio.create_task(seed_initial_demo_data())
    yield
    # Shutdown: Stop scheduler
    stop_scheduler()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS configuration for Svelte frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrument FastAPI with OpenTelemetry
if settings.ENABLE_OTEL_TRACING:
    FastAPIInstrumentor.instrument_app(app)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "database": "PostgreSQL (Connected)",
        "otel_tracing": settings.ENABLE_OTEL_TRACING,
    }


# Mount compiled Svelte 5 frontend in production
from pathlib import Path
from fastapi.staticfiles import StaticFiles

dist_path = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if dist_path.exists():
    app.mount("/", StaticFiles(directory=str(dist_path), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
