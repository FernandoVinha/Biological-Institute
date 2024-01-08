from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os
import json
import bitcoin_rpc

def get_rpc_connection(wallet_name=""):
    rpc_user = "teste"  # Substitua pelo seu nome de usuário RPC
    rpc_password = "teste"  # Substitua pela sua senha RPC
    rpc_host = "localhost"  # Se o Bitcoin Core estiver em execução na mesma máquina
    rpc_port = 8332  # Porta padrão para o RPC do Bitcoin Core

    wallet_path = f"wallet/{wallet_name}" if wallet_name else ""
    return AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/{wallet_path}")

def load_wallet(wallet_name):
    try:
        rpc_connection = get_rpc_connection()
        loaded_wallets = rpc_connection.listwallets()

        if wallet_name in loaded_wallets:
            return  # Carteira já está carregada

        rpc_connection.loadwallet(wallet_name)
        # Carteira carregada com sucesso

    except JSONRPCException as e:
        # Erro ao carregar a carteira
        pass

def create_and_load_standard_wallet(wallet_name):
    rpc_connection = get_rpc_connection()
    
    # Tentando criar a carteira
    print(f"Tentando criar a carteira: {wallet_name}")
    try:
        rpc_connection.createwallet(wallet_name, False)
        print(f"Carteira {wallet_name} criada com sucesso.")
    except JSONRPCException as e:
        print(f"Erro ao criar a carteira {wallet_name}: {e}")

    # Tentando carregar a carteira
    print(f"Tentando carregar a carteira: {wallet_name}")
    try:
        load_wallet(wallet_name)
        print(f"Carteira {wallet_name} carregada com sucesso.")
    except JSONRPCException as e:
        print(f"Erro ao carregar a carteira {wallet_name}: {e}")



def create_and_load_hd_wallet(wallet_name):
    rpc_connection = get_rpc_connection()
    try:
        # Crie uma nova carteira HD
        # No Bitcoin Core 0.21 e posterior, as carteiras são HD por padrão
        create_wallet_response = rpc_connection.createwallet(wallet_name)
        print("Resposta do createwallet:")
        print(create_wallet_response)

        # Carregar a carteira criada
        load_wallet_response = rpc_connection.loadwallet(wallet_name)
        print("Resposta do loadwallet:")
        print(load_wallet_response)

    except JSONRPCException as e:
        print(f"Erro RPC: {e}")

def load_all_wallets(wallets_directory):
    try:
        # Listar todos os diretórios na pasta wallets
        wallets = next(os.walk(wallets_directory))[1]

        for wallet_name in wallets:
            try:
                rpc_connection = get_rpc_connection()
                load_wallet_response = rpc_connection.loadwallet(wallet_name)
                print(f"Carteira '{wallet_name}' carregada com sucesso.")
            except JSONRPCException as e:
                print(f"Erro ao carregar a carteira '{wallet_name}': {e}")

    except Exception as e:
        print(f"Erro ao listar carteiras: {e}")


def new_address(user_wallet_name, superuser_wallet_name):
    try:
        print("Conectando à carteira do usuário...")
        rpc_connection = get_rpc_connection(user_wallet_name)
        print("Criando novo endereço...")
        new_address = rpc_connection.getnewaddress()

        print("Exportando chave privada do novo endereço...")
        private_key = rpc_connection.dumpprivkey(new_address)

        print("Conectando à carteira HD do superusuário...")
        rpc_connection = get_rpc_connection(superuser_wallet_name)
        print("Importando chave privada para a carteira do superusuário...")
        rpc_connection.importprivkey(private_key, "imported_address", False)

        print("Endereço criado com sucesso:", new_address)
        return str(new_address)

    except JSONRPCException as e:
        print(f"Erro RPC: {e}")
        return None




def get_wallet_transactions(wallet_name):
    try:
        rpc_connection = get_rpc_connection(wallet_name)

        # Obtém as transações da carteira
        transactions = rpc_connection.listtransactions("*", 150, 0, True)
        
        # Formata as transações para um formato amigável
        formatted_transactions = []
        for tx in transactions:
            formatted_transaction = {
                "txid": tx["txid"],
                "amount": tx["amount"],
                "confirmations": tx["confirmations"],
                "time": tx["time"],
                "details": tx.get("details", [])
            }
            formatted_transactions.append(formatted_transaction)

        # Retorna as transações em formato JSON
        return json.dumps(formatted_transactions)

    except JSONRPCException as e:
        print(f"Erro RPC: {e}")
        return json.dumps([])  # Retorna uma lista vazia em caso de erro

# Outras funções do bitcoin_rpc.py podem ser adicionadas aqui conforme necessário

# Caminho para a pasta wallets
