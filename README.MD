# Trading System API

## Descrição do Projeto

O **Trading System API** é uma aplicação desenvolvida em Python utilizando o framework **FastAPI**. O objetivo principal é fornecer uma API para gerenciar operações de trading do projeto Tech Challenge 3, incluindo abertura e fechamento de ordens, consulta de métricas de desempenho e integração com serviços externos, como Binance e RDS postegres AWS.

---

## Arquitetura do Projeto

A arquitetura do projeto segue uma estrutura modular e bem organizada, dividida em camadas para facilitar a manutenção e escalabilidade. Abaixo está uma visão geral dos principais componentes:

### 1. **Camada de API**
- **`api/v1/api.py`**: Define os endpoints principais da API e organiza os routers.
- **`api/endpoints/manage_metrics.py`**: Gerencia as métricas de trading.
- **`api/endpoints/manage_trading.py`**: Gerencia as operações de trading, como abertura e fechamento de ordens.
- **`api/endpoints/manage_orders.py`**: (não incluído nos arquivos fornecidos, mas referenciado na arquitetura).

### 2. **Camada de Serviços**
- **`core/services/binance_client.py`**: Integração com a API da Binance para operações de trading.
- **`core/services/rdsConnect.py`**: Gerencia a conexão com o banco de dados PostgreSQL utilizando o AWS RDS.

### 3. **Camada de Utilitários**
- **`api/utils/functions/binance_functions.py`**: Para a Versão 1 do projeto ainda não esta sendo utilizada a abertura de fato das ordens na binance.
- **`api/utils/functions/rds_dml_functions.py`**: Contém funções para manipulação de dados no banco de dados, como inserção, atualização e consulta.

### 4. **Configuração**
- **`core/config.py`**: Gerencia as configurações do projeto, como variáveis de ambiente e configurações específicas para produção e desenvolvimento.
- **`parameterStoreAws.py`**: Integração com o AWS Parameter Store para recuperar segredos e configurações sensíveis.

### 5. **Aplicação Principal**
- **`main.py`**: Ponto de entrada da aplicação. Configura o FastAPI, middleware de CORS e inicializa os routers.

---

## Funcionalidades

### 1. **Gerenciamento de Métricas**
- **Endpoint**: `/api/v1/manageMetrics/getMetrics`
- **Descrição**: Retorna métricas de desempenho de trading, como taxa de sucesso, capital final, drawdown máximo, entre outros.
- **Código Relacionado**: `manage_metrics.py`, `rds_dml_functions.py`.

### 2. **Gerenciamento de Trading**
- **Endpoint**: `/api/v1/manageTrading/SendTrade`
- **Descrição**: Recebe uma ação de trading (compra, venda ou hold) e processa a operação no banco de dados.
- **Payload**:
  ```json
  {
    "action": "1",  // 1 = Compra, 0 = Venda, 2 = Hold
    "close": 100.0  // Preço de fechamento
  }

## Instalação

1. Clone o repositório:
```bash
-  git clone https://github.com/Renatmf5/FastAPI-Trading-tc3.git
-  cd FastAPI-Trading-tc3
```
2. Instale as dependências:
```bash
- pip install -r requirements.txt
```