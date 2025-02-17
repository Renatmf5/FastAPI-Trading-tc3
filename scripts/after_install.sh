#!/bin/bash
DIR="/home/ec2-user/fastapi-app"
echo "AfterInstall: Instalando dependências"
sudo chown -R ec2-user:ec2-user ${DIR}
cd ${DIR}

# Criar ambiente virtual e instalar dependências
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Criar arquivo de serviço systemd para a aplicação
sudo bash -c 'cat <<EOF > /etc/systemd/system/fastapi-app.service
[Unit]
Description=First FastAPI Application
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/fastapi-app
ExecStart=/home/ec2-user/fastapi-app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 80 > app.log 2>&1 &
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

# Recarregar systemd para aplicar as mudanças
sudo systemctl daemon-reload