from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CareerBoost API",
    description="AI-powered interview prep, typing practice & job portal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health_check():
    """Health check — returns 200 if API is running."""
    return {
        "status": "ok",
        "service": "CareerBoost API",
        "version": "1.0.0"
    }
    