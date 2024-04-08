#!/bin/bash

# Definir o caminho do diretório do projeto Django
PROJECT_DIR=$(pwd)
SERVICE_NAME="instituto_biologico"

# Criar e ativar o ambiente virtual
echo "Criando e ativando o ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar ngrok se não estiver instalado
if ! command -v ngrok &> /dev/null
then
    echo "Instalando ngrok..."
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update
    sudo apt install ngrok
fi

# Instalar as dependências do projeto Django dentro do ambiente virtual
echo "Instalando as dependências do projeto Django dentro do ambiente virtual..."
pip install -r requirements.txt

# Configurar o authtoken do ngrok
echo "Configurando o authtoken do ngrok..."
ngrok config add-authtoken 2emv4xRVSt3Jj3oTxkgq0BdRfDM_3SsdzXWCcf1Vj4az1qnFF

# Criar o script de inicialização do Instituto Biológico
echo "Criando script de inicialização do Instituto Biológico..."
echo "#!/bin/bash
cd $PROJECT_DIR

# Iniciar servidor Django na porta 8000
python manage.py runserver 0.0.0.0:8000 &

# Aguardar até que o Django esteja executando
sleep 10

# Iniciar ngrok
ngrok http http://0.0.0.0:8000/" > start_instituto_biologico.sh

# Tornar o script de inicialização executável
chmod +x start_instituto_biologico.sh

# Criar o arquivo de serviço systemd para o Instituto Biológico
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

echo "[Unit]
Description=Iniciar Servidor do Instituto Biológico e ngrok na inicialização

[Service]
ExecStart=$PROJECT_DIR/start_instituto_biologico.sh
User=root

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE

# Recarregar os daemons do systemd, habilitar e iniciar o serviço do Instituto Biológico
echo "Configurando e iniciando o serviço systemd do Instituto Biológico..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "Instalação do serviço do Instituto Biológico concluída!"
