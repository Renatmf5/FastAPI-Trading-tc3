from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from core.services.binance_client import client
from api.utils.functions.binance_functions import *
from api.utils.functions.rds_dml_functions import *

router = APIRouter()

# Modelo para validar o payload recebido
class TradePayload(BaseModel):
    action: str
    close: float

@router.post("/SendTrade")
async def send_trade(payload: TradePayload):
    try:
        # Processar os dados recebidos
        action = payload.action
        close = payload.close

        if action == "2":
            # Ordem de hold
            return JSONResponse(content={"message": "Ordem de Hold", "action": action}, media_type="application/json")
        elif action == "1":
            # Ordem de compra
            # Chamar a função de métricas como exemplo
            status_trading = get_status_trade()
            status_trading_dict = json.loads(status_trading)
            
            # verifica se status_trading tem conteudo
            if "error" in status_trading_dict:
                # abrir ordem de compra
                open_order_trading(close, "BUY", 1000)
                return JSONResponse(content={"message": "Ordem de compra aberta com sucesso", "action": action}, media_type="application/json")
            # Carregar o JSON retornado e acessar o campo "status"
            
            # fechar uma venda
            if status_trading_dict["status"] == "OPEN" and status_trading_dict["side"] == "SELL":
                # fechar ordem de venda
                trade_id = status_trading_dict["trade_id"]
                entry_price = status_trading_dict["entry_price"]
                quantity = status_trading_dict["current_value"] / entry_price
                profit = (entry_price - close) * quantity
                current_value = status_trading_dict["current_value"] + profit
                trade_return = (profit / status_trading_dict["current_value"]) * 100
                success = profit > 0
                close_order_trading(trade_id, entry_price, close, profit, success, trade_return, current_value)
                return JSONResponse(content={"message": "Fechamento de trade de venda com sucesso", "action": action}, media_type="application/json")
                
            elif status_trading_dict["status"] == "CLOSED":
                # abrir ordem de compra
                open_order_trading(close, "BUY", status_trading_dict["current_value"])    

        elif action == "0":
            # Ordem de venda
            status_trading = get_status_trade()
            status_trading_dict = json.loads(status_trading)
            
            # verifica se status_trading tem conteudo
            if "error" in status_trading_dict:
                # abrir ordem de compra
                open_order_trading(close, "SELL", 1000)
                return JSONResponse(content={"message": "Ordem de venda aberta com sucesso", "action": action}, media_type="application/json")
            

            # Fechar posição de compra, se existir
            if status_trading_dict["status"] == "OPEN" and status_trading_dict["side"] == "BUY":
                trade_id = status_trading_dict["trade_id"]
                entry_price = status_trading_dict["entry_price"]
                quantity = status_trading_dict["current_value"] / entry_price
                profit = (close - entry_price) * quantity
                current_value = status_trading_dict["current_value"] + profit
                trade_return = (profit / status_trading_dict["current_value"]) * 100
                success = profit > 0
                close_order_trading(trade_id, entry_price, close, profit, success, trade_return,current_value)
                return JSONResponse(content={"message": "Fechamento de trade de compra com sucesso", "action": action}, media_type="application/json")
            
            elif status_trading_dict["status"] == "CLOSED":
                # abrir ordem de venda
                open_order_trading(close, "SELL", status_trading_dict["current_value"])
                
        # criar chamada que atualiza o unrealizedpnl com base no close e o entry_price e o side da ordem
        if status_trading_dict["status"] == "OPEN" and status_trading_dict["side"] == "BUY":
            trade_id = status_trading_dict["trade_id"]
            entry_price = status_trading_dict["entry_price"]
            quantity = status_trading_dict["current_value"] / entry_price
            unrealizedPnl = (close - entry_price) * quantity
            update_unrealized_pnl(trade_id, unrealizedPnl)
        elif status_trading_dict["status"] == "OPEN" and status_trading_dict["side"] == "SELL":
            trade_id = status_trading_dict["trade_id"]
            entry_price = status_trading_dict["entry_price"]
            quantity = status_trading_dict["current_value"] / entry_price
            unrealizedPnl = (entry_price - close) * quantity
            update_unrealized_pnl(trade_id, unrealizedPnl)

        # Retornar resposta de sucesso
        return JSONResponse(content={"message": "Dados processados com sucesso", "action": action}, media_type="application/json")
    except Exception as e:
        print(f"Erro ao processar a solicitação: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a solicitação")
    
@router.get("/GetTrade")
async def get_trade():
    try:
        trades = get_list_trades()
        
        if not isinstance(trades, list):
            trades = [trades]  # Garante que sempre retorna uma lista
        return JSONResponse(content=trades, media_type="application/json")
    except Exception as e:
        print(f"Erro ao obter o status da ordem: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao obter o status da ordem")