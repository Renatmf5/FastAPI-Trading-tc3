from fastapi import APIRouter
from .endpoints import manage_orders


api_router = APIRouter()

api_router.include_router(manage_orders.router, prefix="/manageOrders", tags=["getOpenPositions"])


@api_router.get("/")
async def root():
    return {"message": "Hello World"}