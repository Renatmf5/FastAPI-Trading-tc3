from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.api import api_router
from core.config import settings
import os
import uvicorn

def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    
    # Configuração do CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Pode restringir para ["http://localhost:3000"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Adicionando os routers
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    @app.get("/")
    def read_root():
        return {"message": "API is running"}
    
    return app

app = get_application()

if __name__ == "__main__":
    env = os.getenv("ENV", "development")
    host = "0.0.0.0"
    port = 80 if env == "production" else 8000
    log_level = settings.LOG_LEVEL
    
    uvicorn.run("main:app", host=host, port=port, log_level=log_level, reload=(env != "production"))
