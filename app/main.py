from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter 
from app.api.api import api_router


def create_tables():
    Base.metadata.create_all(bind=engine)

def drop_tables():
    Base.metadata.drop_all(bind=engine)

def get_application() -> FastAPI:
    app = FastAPI(
        title="Library Management API",
        description="API for Library Management System",
        version="1.0.0"
    )

    # Register limiter and exception handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)


    # Include routers
    app.include_router(api_router, prefix="/api/v1")

    # drop_tables()
    create_tables()



    return app

app = get_application()

@app.get("/")
def root():
    return {"message": "Library Management API is running!"}
