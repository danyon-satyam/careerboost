from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, users, jobs, interviews, typing, analytics

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

# Register routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(interviews.router, prefix="/api/v1")
app.include_router(typing.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
def health_check():
    """Health check — returns 200 if API is running."""
    return {
        "status": "ok",
        "service": "CareerBoost API",
        "version": "1.0.0"
    }
