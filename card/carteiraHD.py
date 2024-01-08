from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Configurações de RPC do Bitcoin Core
rpc_user = "teste"  # Substitua pelo seu nome de usuário RPC
rpc_password = "teste"  # Substitua pela sua senha RPC
rpc_host = "localhost"  # Se o Bitcoin Core estiver em execução na mesma máquina
rpc_port = 8332  # Porta padrão para o RPC do Bitcoin Core

# Crie uma conexão RPC com o Bitcoin Core
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

try:
    # Nome do arquivo de carteira
    wallet_name = "minha_carteira_hd"

    # Crie uma nova carteira HD
    # No Bitcoin Core 0.21, as carteiras são HD por padrão
    create_wallet_response = rpc_connection.createwallet(wallet_name)
    print("Resposta do createwallet:")
    print(create_wallet_response)

    # Carregar a carteira criada
    load_wallet_response = rpc_connection.loadwallet(wallet_name)
    print("Resposta do loadwallet:")
    print(load_wallet_response)

except JSONRPCException as e:
    print(f"Erro RPC: {e}")


