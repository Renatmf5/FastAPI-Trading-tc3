from fastapi import APIRouter
from fastapi.responses import JSONResponse
from core.services.binance_client import client
from api.utils.functions.binance_functions import *
from api.utils.functions.rds_dml_functions import *

router = APIRouter()

@router.get("/getMetrics")
async def get_open_orders():
    try:
        data = get_metrics()
        #print(f"Posições retornadas pela API: {positions}")  # Log de depuração
        if not isinstance(data, list):
            data = [data]  # Garante que sempre retorna uma lista
        return JSONResponse(content=data, media_type="application/json")
    except Exception as e:
        print(f"Erro ao obter metricas: {e}")
        return None