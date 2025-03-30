from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

# Import routers (placeholders, you'll define these endpoints later)
# from app.api.api import api_router

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_application() -> FastAPI:
    app = FastAPI(
        title="Library Management API",
        description="API for Library Management System",
        version="1.0.0"
    )

    # Include your API routers here
    # app.include_router(api_router, prefix="/api/v1")

    # Create tables on startup (only for initial/demo purposes)
    create_tables()

    return app

app = get_application()

@app.get("/")
def root():
    return {"message": "Library Management API is running!"}
