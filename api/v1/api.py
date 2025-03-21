from fastapi import APIRouter
from .endpoints import manage_orders, manage_metrics, manage_trading


api_router = APIRouter()

api_router.include_router(manage_orders.router, prefix="/manageOrders", tags=["getOpenPositions"])
api_router.include_router(manage_metrics.router, prefix="/manageMetrics", tags=["getMetrics"])
api_router.include_router(manage_trading.router, prefix="/manageTrading", tags=["postTrading"])


@api_router.get("/")
async def root():
    return {"message": "Hello World"}