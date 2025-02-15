from core.services.rdsConnect import db_instance
import psycopg2

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