from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Configurações de RPC do Bitcoin Core
rpc_user = "teste"  # Substitua pelo seu nome de usuário RPC
rpc_password = "teste"  # Substitua pela sua senha RPC
rpc_host = "localhost"  # Se o Bitcoin Core estiver em execução na mesma máquina
rpc_port = 8332  # Porta padrão para o RPC do Bitcoin Core

# Crie uma conexão RPC com o Bitcoin Core
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

try:
    # Crie uma nova carteira
    wallet_name = "1"
    rpc_connection.createwallet(wallet_name, False)  # O segundo parâmetro define se a carteira é de observação (False para uma carteira padrão)

    # Gere um novo endereço na carteira
    new_address = rpc_connection.getnewaddress(wallet_name)

    # Obtenha a chave privada correspondente ao endereço gerado
    private_key = rpc_connection.dumpprivkey(new_address)

    print(f"Endereço Bitcoin: {new_address}")
    print(f"Chave Privada: {private_key}")

except JSONRPCException as e:
    print(f"Erro RPC: {e}")
