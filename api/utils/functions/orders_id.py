class OrderIds:
    def __init__(self):
        self.open_order_id = None
        self.stop_order_id = None
        self.profit_order_id = None

    def update_order_ids(self, open_order_id, stop_order_id, profit_order_id):
        self.open_order_id = open_order_id
        self.stop_order_id = stop_order_id
        self.profit_order_id = profit_order_id

    def get_order_ids(self):
        return self.open_order_id, self.stop_order_id, self.profit_order_id

# Instância global do OrderManager
Order_Ids = OrderIds()