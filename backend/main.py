from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda: None

from api import brand_routes, content, feedback, product, recent, trends
from database.database import init_db

load_dotenv(Path(__file__).resolve().parent / ".env")
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="TrendPilot AI Backend",
    description="MVP backend for AI short-form content generation.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product.router)
app.include_router(content.router)
app.include_router(feedback.router)
app.include_router(recent.router)
app.include_router(brand_routes.router)
app.include_router(trends.router)


@app.get("/")
def root():
    return {"name": "TrendPilot AI", "status": "ready"}


@app.get("/api/health")
def health_check():
    return {"ok": True, "service": "trendpilot-backend"}
