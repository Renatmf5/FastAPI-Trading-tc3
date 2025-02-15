from fastapi import APIRouter
from core.services.binance_client import client
from api.utils.functions.binance_functions import *
from api.utils.functions.rds_dml_functions import *
from api.utils.functions.orders_id import Order_Ids

router = APIRouter()

@router.get("/getOpenPositions")
async def get_open_orders(symbol: str):
    try:
        positions = client.futures_position_information(symbol=symbol, recvWindow=60000)
        #print(f"Posições retornadas pela API: {positions}")  # Log de depuração
        for position in positions:
            if float(position['positionAmt']) != 0:
                return position
        return None
    except Exception as e:
        print(f"Erro ao obter posições abertas: {e}")
        return None
    

@router.get("/OpenPosition")
async def openOrders(symbol: str, prediction: float, target: float, leverage: int = 2):
    
    open_id, stop_id, profit_id = Order_Ids.get_order_ids()
    get_trade_statistics(open_id, stop_id, profit_id)
    
    # Verificar e registrar as estatísticas de negociação das ordens anteriores
    if open_id and (stop_id or profit_id):
        get_trade_statistics(open_id, stop_id, profit_id)
    
    #transformar prediction em int
    prediction = int(prediction)
    
    target_maior = 1+target
    target_menor = 1-target
    
    current_price = get_current_price(symbol) 
    
    if current_price is None:
        # retorna erro
        return {"message": "Erro ao obter o preço corrente"}
    
    balance = get_account_balance()
    if balance is None:
        return {"message": "Erro ao obter o saldo da conta"}
    
    
    # Define a alavancagem para o símbolo
    set_leverage(symbol, leverage)
    
    # Calcula a quantidade de BTC para a ordem
    quantity = calculate_order_quantity(balance, current_price, leverage)
    
    # Define o lado da posição
    position_side = 'LONG' if prediction == 1 else 'SHORT'
    
    if prediction == 0:
        # Ordem de venda
        stop_loss = current_price * target_maior  # Stop loss maior que o valor atual
        take_profit = current_price * target_menor  # Take profit menor que o valor atual
        OpenOrder_id, StopOrder_id, ProfitOrder_id = place_order(symbol, 'SELL', quantity, stop_loss, take_profit, position_side)
    elif prediction == 1:
        # Ordem de compra
        stop_loss = current_price * target_menor  # Stop loss menor que o valor atual
        take_profit = current_price * target_maior  # Take profit maior que o valor atual
        OpenOrder_id, StopOrder_id, ProfitOrder_id = place_order(symbol, 'BUY', quantity, stop_loss, take_profit, position_side)
    else:
        print(f"Previsão {prediction}. Nenhuma ordem será aberta.")
        return {"message": f"Previsão {prediction}. Nenhuma ordem será aberta."}
    
    # Inserir as ordens no banco de dados
    insert_orders(OpenOrder_id, StopOrder_id, ProfitOrder_id, position_side, quantity, current_price, 0)
    
    # Atualizar os IDs das ordens
    Order_Ids.update_order_ids(OpenOrder_id, StopOrder_id, ProfitOrder_id)
    # Insere o balance na tabela balances
    insert_balance(balance)
    
    return {"message": "Ordem aberta com sucesso"}
    