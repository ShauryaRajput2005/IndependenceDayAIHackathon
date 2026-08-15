"""
main.py — TrendPilot AI FastAPI application entry point.

Run: uvicorn main:app --reload
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import get_settings
from database.database import init_db
from api import product, content, feedback, recent
from utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Handle startup and shutdown events."""
    logger.info("TrendPilot AI backend starting up…")
    init_db()
    logger.info("Startup complete. Frontend origin: %s", get_settings().frontend_url)
    yield
    logger.info("TrendPilot AI backend shutting down.")


# ── Application factory ───────────────────────────────────────────────────────

app = FastAPI(
    title="TrendPilot AI",
    description=(
        "AI-powered viral content generator. "
        "Supply product information and receive hooks, scripts, memes, captions and GIFs."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(product.router)
app.include_router(content.router)
app.include_router(feedback.router)
app.include_router(recent.router)

# ── Health endpoint ───────────────────────────────────────────────────────────

@app.get("/api/health", tags=["Health"], summary="Service health check")
def health_check():
    """Returns service status. Use to verify the backend is running."""
    return {"status": "ok", "service": "trendpilot-backend"}

# ── Global exception handlers ─────────────────────────────────────────────────

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal error occurred."},
    )
