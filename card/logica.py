from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Configurações de RPC do Bitcoin Core
rpc_user = "teste"  # Substitua pelo seu nome de usuário RPC
rpc_password = "teste"  # Substitua pela sua senha RPC
rpc_host = "localhost"  # Se o Bitcoin Core estiver em execução na mesma máquina
rpc_port = 8332  # Porta padrão para o RPC do Bitcoin Core

# Função para realizar cada etapa individualmente
def perform_step(step_description, callback):
    proceed = input(f"{step_description}. Deseja continuar? (S/n): ")
    if proceed.lower() != 'n':
        callback()
    else:
        print("Operação cancelada.")

# Etapa 1: Acessar a carteira '1'
def access_wallet_1():
    global rpc_connection
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")
    print("Conexão RPC estabelecida com a carteira '1'.")

# Etapa 2: Criar um novo endereço na carteira '1'
def create_new_address():
    global new_address
    new_address = rpc_connection.getnewaddress("")
    print(f"Novo endereço Bitcoin na carteira '1': {new_address}")

# Etapa 3: Exportar a chave privada da carteira '1'
def export_private_key():
    global private_key
    private_key = rpc_connection.dumpprivkey(new_address)
    print(f"Chave Privada da carteira '1': {private_key}")

# Etapa 4: Acessar a carteira HD 'minha_carteira_hd'
def access_hd_wallet():
    global rpc_connection
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/minha_carteira_hd")
    print("Conexão RPC estabelecida com a carteira HD 'minha_carteira_hd'.")

# Etapa 5: Importar o endereço da carteira '1' na carteira HD 'minha_carteira_hd'
def import_address_to_hd_wallet():
    import_key_response = rpc_connection.importprivkey(private_key, "label", False)  # Alterado aqui
    print(f"Resposta do importprivkey para a carteira HD 'minha_carteira_hd': {import_key_response}")


# Etapa 6: Listar todos os endereços na carteira HD 'minha_carteira_hd'
def list_addresses_in_hd_wallet():
    addresses = rpc_connection.listreceivedbyaddress(0, True)
    print("Endereços na carteira HD 'minha_carteira_hd':")
    for address_info in addresses:
        address = address_info["address"]
        label = address_info.get("label", "Sem rótulo")
        print(f"Endereço: {address}, Rótulo: {label}")

# Executar as etapas sequencialmente
perform_step("Acessar a carteira '1'", access_wallet_1)
perform_step("Criar um novo endereço na carteira '1'", create_new_address)
perform_step("Exportar a chave privada da carteira '1'", export_private_key)
perform_step("Acessar a carteira HD 'minha_carteira_hd'", access_hd_wallet)
perform_step("Importar o endereço da carteira '1' na carteira HD 'minha_carteira_hd'", import_address_to_hd_wallet)

# Etapa adicional: Listar todos os endereços na carteira HD 'minha_carteira_hd'
perform_step("Listar todos os endereços na carteira HD 'minha_carteira_hd'", list_addresses_in_hd_wallet)
