from core.services.rdsConnect import db_instance
import psycopg2
import json
from datetime import datetime
from decimal import Decimal

def execute_query(query, params):
    connection = db_instance.get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
    except psycopg2.OperationalError as e:
        print(f"Erro operacional: {e}")
        if connection and not connection.closed:
            connection.rollback()
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        if connection and not connection.closed:
            connection.rollback()
    finally:
        db_instance.release_connection(connection)

def insert_balance(balance):
    query = """
    INSERT INTO balances (user_id, balance)
    VALUES (1,%s)
    """
    params = (balance,)
    execute_query(query, params)

def insert_orders(OpenOrder_id, StopOrder_id, ProfitOrder_id, side, quantity, price, amount_fee):
    insert1 = """
    INSERT INTO Orders (order_id, user_id, crypto_id, order_type, side, quantity, price, status, amount_fee)
    VALUES (%s,2,1,'MARKET',%s,%s,%s,'NEW',%s)
    """
    params1 = (OpenOrder_id, side, quantity, price, amount_fee)
    
    insert2 = """
    INSERT INTO Orders (order_id, user_id, crypto_id, order_type, side, quantity, price, status, amount_fee)
    VALUES (%s,2,1,'STOP',%s,%s,%s,'NEW',%s)
    """
    params2 = (StopOrder_id, side, quantity, price, amount_fee)
    
    insert3 = """
    INSERT INTO Orders (order_id, user_id, crypto_id, order_type, side, quantity, price, status, amount_fee)
    VALUES (%s,2,1,'PROFIT',%s,%s,%s,'NEW',%s)
    """
    params3 = (ProfitOrder_id, side, quantity, price, amount_fee)
    
    connection = db_instance.get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(insert1, params1)
            cursor.execute(insert2, params2)
            cursor.execute(insert3, params3)
            connection.commit()
    except psycopg2.OperationalError as e:
        print(f"Erro operacional: {e}")
        if connection and not connection.closed:
            connection.rollback()
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        if connection and not connection.closed:
            connection.rollback()
    finally:
        db_instance.release_connection(connection)

def insert_trade(order_id, linked_order_id, profit_loss, fee_amount, success, percent_gain):
    query = """
    INSERT INTO Trades (order_id, linked_order_id, profit_loss, fee_amount, success, percent_gain) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (order_id, linked_order_id, profit_loss, fee_amount, success, percent_gain)
    execute_query(query, params)
    
def get_metrics():
    query = """
    SELECT 
        batch_id,
        total_trades,
        win_rate,
        avg_trade_duration,
        avg_profit_pct,
        avg_loss_pct,
        final_capital,
        max_gain,
        max_loss,
        max_drawdown,
        max_consecutive_gains,
        max_consecutive_losses,
        stop_loss_count,
        take_profit_count,
        long_trades_count,
        short_trades_count,
        start_time,
        end_time,
        win_count,
        loss_count, 
        final_gross_capital
        
    FROM trade_metrics
    WHERE batch_id = (SELECT MAX(batch_id) FROM trade_metrics)
    """
    
    connection = db_instance.get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            metrics_list = []
            for result in results:
                metrics = {
                    "batch_id": result[0],
                    "total_trades": result[1],
                    "win_rate": result[2],
                    "avg_trade_duration": result[3],
                    "avg_profit_pct": result[4],
                    "avg_loss_pct": result[5],
                    "final_capital": result[6],
                    "max_gain": result[7],
                    "max_loss": result[8],
                    "max_drawdown": result[9],
                    "max_consecutive_gains": result[10],
                    "max_consecutive_losses": result[11],
                    "stop_loss_count": result[12],
                    "take_profit_count": result[13],
                    "long_trades_count": result[14],
                    "short_trades_count": result[15],
                    "start_time": result[16].isoformat() if isinstance(result[16], datetime) else result[16],
                    "end_time": result[17].isoformat() if isinstance(result[17], datetime) else result[17],
                    'win_count': result[18],
                    'loss_count': result[19],
                    'final_gross_capital': int(result[20]) if isinstance(result[20], Decimal) else result[20]
                }
                metrics_list.append(metrics)
            return json.dumps(metrics_list)
    except psycopg2.OperationalError as e:
        print(f"Erro operacional: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return json.dumps({"error": "Erro operacional"})
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return json.dumps({"error": "Erro ao executar a consulta"})
    finally:
        db_instance.release_connection(connection)

def get_list_trades():
    query = """
    SELECT 
        side,
        entry_price,
        exit_price,
        status,
        profit_loss,
        success,
        trade_return,
        unrealizedPnl,
        current_value,
        created_at,
        updated_at        
    FROM trades_trading
    ORDER BY created_at DESC
    """
    
    connection = db_instance.get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            metrics_list = []
            for result in results:
                metrics = {
                    "side": result[0],
                    "entry_price": float(result[1]) if isinstance(result[1], Decimal) else result[1],
                    "exit_price": float(result[2]) if isinstance(result[2], Decimal) else result[2],
                    "status": result[3],
                    "profit_loss": float(result[4]) if isinstance(result[4], Decimal) else result[4],
                    "success": result[5],
                    "trade_return": float(result[6]) if isinstance(result[6], Decimal) else result[6],
                    "unrealizedPnl": float(result[7]) if isinstance(result[7], Decimal) else result[7],
                    "current_value": float(result[8]) if isinstance(result[8], Decimal) else result[8],
                    "created_at": result[9].isoformat() if isinstance(result[9], datetime) else result[9],
                    "updated_at": result[10].isoformat() if isinstance(result[10], datetime) else result[10],
                }
                metrics_list.append(metrics)
            return json.dumps(metrics_list)
    except psycopg2.OperationalError as e:
        print(f"Erro operacional: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return json.dumps({"error": "Erro operacional"})
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return json.dumps({"error": "Erro ao executar a consulta"})
    finally:
        db_instance.release_connection(connection)
        
def get_status_trade():
    query = """
    SELECT 
        trade_id,
        side,
        entry_price,
        status,
        current_value   
    FROM trades_trading
    WHERE trade_id = (SELECT MAX(trade_id) FROM trades_trading)
    """
    connection = db_instance.get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                trade_status = {
                    "trade_id": result[0],
                    "side": result[1],
                    "entry_price": float(result[2]) if isinstance(result[2], Decimal) else result[2],
                    "status": result[3],
                    "current_value": float(result[4]) if isinstance(result[4], Decimal) else result[4]
                    
                }
                return json.dumps(trade_status)
            else:
                return json.dumps({"error": "Nenhum dado encontrado"})
    except psycopg2.OperationalError as e:
        print(f"Erro operacional: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return json.dumps({"error": "Erro operacional"})
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return json.dumps({"error": "Erro ao executar a consulta"})
    finally:
        db_instance.release_connection(connection)
        
def close_order_trading(trade_id, entry_price, exit_price, profit, success, trade_return, current_value):
    query = """
    UPDATE trades_trading
    SET entry_price = %s,
        exit_price = %s,
        profit_loss = %s,
        success = %s,
        trade_return = %s,
        status = 'CLOSED',
        unrealizedPnl = 0,
        current_value = %s,
        updated_at = NOW()
    WHERE trade_id = %s
    """
    params = (entry_price, exit_price, profit, success, trade_return,current_value, trade_id)
    connection = db_instance.get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
        return {"message": f"Ordem {trade_id} fechada com sucesso."}
    except psycopg2.OperationalError as e:
        print(f"Erro operacional: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return {"error": f"Erro operacional ao fechar a ordem {trade_id}: {e}"}
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return {"error": f"Erro ao fechar a ordem {trade_id}: {e}"}
    finally:
        db_instance.release_connection(connection)


def open_order_trading(entry_price, side, initial_value=None):
    if initial_value:
        query = """
        INSERT INTO trades_trading (entry_price, side, status, current_value, created_at)
        VALUES (%s, %s, 'OPEN', %s, NOW())
        """
        params = (entry_price, side, initial_value)
    else:
        query = """
        INSERT INTO trades_trading (entry_price, side, status, created_at)
        VALUES (%s, %s, 'OPEN', NOW())
        """
        params = (entry_price, side)
    connection = db_instance.get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
        return {"message": f"Nova ordem aberta com sucesso no lado {side} com preço de entrada {entry_price}."}
    except psycopg2.OperationalError as e:
        print(f"Erro operacional: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return {"error": f"Erro operacional ao abrir nova ordem: {e}"}
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return {"error": f"Erro ao abrir nova ordem: {e}"}
    finally:
        db_instance.release_connection(connection)
        
    
def update_unrealized_pnl(trade_id, unrealizedPnl):
    query = """
    UPDATE trades_trading
    SET unrealizedPnl = %s
    WHERE trade_id = %s
    """
    params = (unrealizedPnl, trade_id)
    connection = db_instance.get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
        return {"message": f"Unrealized PnL atualizado com sucesso para a ordem {trade_id}."}
    except psycopg2.OperationalError as e:
        print(f"Erro operacional: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return {"error": f"Erro operacional ao atualizar o Unrealized PnL: {e}"}
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        if connection and not connection.closed:
            connection.rollback()
        return {"error": f"Erro ao atualizar o Unrealized PnL: {e}"}
    finally:
        db_instance.release_connection(connection)