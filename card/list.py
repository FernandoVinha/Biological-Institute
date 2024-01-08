from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Configurações de RPC do Bitcoin Core
rpc_user = "teste"  # Substitua pelo seu nome de usuário RPC
rpc_password = "teste"  # Substitua pela sua senha RPC
rpc_host = "localhost"  # Se o Bitcoin Core estiver em execução na mesma máquina
rpc_port = 8332  # Porta padrão para o RPC do Bitcoin Core

# Nome da carteira HD
wallet_name_hd = "minha_carteira_hd"

# Crie uma conexão RPC com o Bitcoin Core
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

try:
    # Lista de rótulos (labels) associados aos endereços
    labels = rpc_connection.listlabels()

    # Lista de endereços associados a cada rótulo
    for label in labels:
        addresses = rpc_connection.listreceivedbylabel(label)
        print(f"Endereços no rótulo '{label}':")
        for address_info in addresses:
            print(f"Endereço: {address_info['address']}")
except JSONRPCException as e:
    print(f"Erro RPC: {e}")