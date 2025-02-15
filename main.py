from fastapi import FastAPI
from api.v1.api import api_router
from core.config import settings

import os

def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/")
    def read_root():
        return {"message": "API is running"}

    return app

app = get_application()

if __name__ == "__main__":
    import uvicorn
    env = os.getenv("ENV", "development")
    if env == "production":
        uvicorn.run("main:app", host="0.0.0.0", port=80, log_level=settings.LOG_LEVEL)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level=settings.LOG_LEVEL, reload=True)