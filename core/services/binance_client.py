from binance.client import Client
from .parameterStoreAws import get_ssm_parameter

# Inicializa o cliente da Binance
client = Client(get_ssm_parameter("/IngestData-app/BINANCE_API_KEY"), get_ssm_parameter("/IngestData-ap/BINANCE_SECRET_KEY"), {"timeout": 20}) 