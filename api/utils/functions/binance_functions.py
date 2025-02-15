from core.services.binance_client import client
from datetime import datetime
import pandas as pd
import boto3


def get_current_price(symbol):
    try:
        ticker = client.futures_symbol_ticker(symbol=symbol, recvWindow=60000)
        return float(ticker['price'])
    except Exception as e:
        print(f"Erro ao obter o preço corrente: {e}")
        return None
    
    
def get_account_balance(asset='USDT'):
    try:
        balance_info = client.futures_account_balance(recvWindow=60000)
        for entry in balance_info:
            if entry['asset'] == asset:
                return float(entry['balance'])
        return None
    except Exception as e:
        print(f"Erro ao obter o saldo da conta: {e}")
        return None
    
def set_leverage(symbol, leverage):
    try:
        response = client.futures_change_leverage(symbol=symbol, leverage=leverage, recvWindow=60000)
    except Exception as e:
        print(f"Erro ao definir a alavancagem: {e}")
        
        
def calculate_order_quantity(balance, current_price, leverage, percentage=0.5):
    usdt_to_use = (balance * percentage) * leverage
    btc_quantity = usdt_to_use / current_price
    
    btc_quantity = round(btc_quantity, 3)

    return btc_quantity

def cancel_all_open_orders(symbol):
    try:
        result = client.futures_cancel_all_open_orders(symbol=symbol, recvWindow=60000)
    except Exception as e:
        print(f"Erro ao cancelar todas as ordens abertas: {e}")
        
def place_order(symbol, side, quantity, stop_loss, take_profit, position_side):
    try:
        # Cancela todas as ordens abertas para o símbolo
        cancel_all_open_orders(symbol)
        
        # Verifica se o valor nocional da ordem é maior ou igual a 100 USDT
        current_price = get_current_price(symbol)
        notional_value = quantity * current_price
        if notional_value < 100:
            print(f"Erro: O valor nocional da ordem ({notional_value} USDT) é menor que 100 USDT.")
            return

        stop_loss = round(stop_loss,1)
        take_profit = round(take_profit,1)
               

        # Abre a ordem de mercado
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity,
            positionSide=position_side,
            recvWindow=60000
        )
        
        stop_loss_order = client.futures_create_order(
            symbol=symbol,
            side='SELL' if side == 'BUY' else 'BUY',
            type='STOP_MARKET',
            stopPrice=stop_loss,  # Preço que dispara a ordem
            quantity=quantity,  # Define a quantidade de contratos a ser vendida
            timeInForce='GTC',
            positionSide=position_side,
            recvWindow=60000
        )

        # Configura o take profit
        take_profit_order = client.futures_create_order(
            symbol=symbol,
            side='SELL' if side == 'BUY' else 'BUY',
            type='TAKE_PROFIT_MARKET',
            stopPrice=take_profit,  # Preço que dispara a ordem
            quantity=quantity,
            timeInForce='GTC',
            positionSide=position_side,
            recvWindow=60000
        )
        
        OpenOrder_id = order['orderId']
        StopOrder_id = stop_loss_order['orderId']
        ProfitOrder_id = take_profit_order['orderId']
        
        return OpenOrder_id, StopOrder_id, ProfitOrder_id

    except Exception as e:
        cancel_all_open_orders(symbol)
        print(f"Erro ao abrir a ordem: {e}")
        
        
        
def get_trade_statistics(open_id, stop_id, profit_id):
    try:
        # Obter histórico de ordens
        orders = client.futures_get_all_orders(recvWindow=60000)
        
        # Converter ordens para dataframe
        orders_df = pd.DataFrame(orders)
        
        # Filtrar ordens pelos IDs fornecidos
        open_order = orders_df[orders_df['orderId'] == open_id]
        stop_order = orders_df[orders_df['orderId'] == stop_id]
        profit_order = orders_df[orders_df['orderId'] == profit_id]
        
        # Verificar se as ordens estão com status 'FILLED'
        if open_order.empty or open_order.iloc[0]['status'] != 'FILLED':
            print(f"Ordem de abertura {open_id} não está preenchida.")
            return
        
        if not stop_order.empty and stop_order.iloc[0]['status'] == 'FILLED':
            linked_order = stop_order.iloc[0]
        elif not profit_order.empty and profit_order.iloc[0]['status'] == 'FILLED':
            linked_order = profit_order.iloc[0]
        else:
            print("Nenhuma ordem de stop ou take profit está preenchida.")
            return
        
        # Calcular profit/loss
        open_price = float(open_order.iloc[0]['avgPrice'])
        linked_price = float(linked_order['avgPrice'])
        quantity = float(open_order.iloc[0]['executedQty'])
        
        if open_order.iloc[0]['side'] == 'BUY':
            profit_loss = (linked_price - open_price) * quantity
        else:
            profit_loss = (open_price - linked_price) * quantity
        
        # Calcular o percentual de ganho
        percent_gain = round((profit_loss / (open_price * quantity)) * 100, 2)

        # Inserir dados no PostgreSQL
        insert_trade(open_id, linked_order['orderId'], profit_loss, 0, success, percent_gain)

        
    except Exception as e:
        print(f"Erro ao obter o histórico de ordens: {e}")
        
        
    
