import requests
import json
import urllib3
import binascii
import os

# Suprimir avisos de requisições HTTPS inseguras (para desenvolvimento/testes)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_macaroon_hex(macaroon_path):
    with open(macaroon_path, 'rb') as macaroon_file:
        macaroon_bytes = macaroon_file.read()
        return binascii.hexlify(macaroon_bytes).decode('utf-8')

def create_lnd_invoice(api_url, api_port, amount, memo, macaroon_hex):
    url = f"https://{api_url}:{api_port}/v1/invoices"
    headers = {
        'Content-Type': 'application/json',
        'Grpc-Metadata-macaroon': macaroon_hex,
    }
    invoice_data = {
        "value": amount,  # Valor da invoice em satoshis
        "memo": memo,     # Descrição da invoice
    }

    response = requests.post(url, headers=headers, data=json.dumps(invoice_data), verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao criar a invoice: {response.status_code} {response.text}")

# Configurações
api_url = "localhost"
api_port = "8081"
amount = 1000  # Valor em satoshis
memo = "Teste Invoice"

# Caminho padrão para o admin.macaroon no LND
home_dir = os.path.expanduser("~")
macaroon_path = os.path.join(home_dir, ".lnd", "data", "chain", "bitcoin", "mainnet", "admin.macaroon")
macaroon_hex = get_macaroon_hex(macaroon_path)

# Criar a invoice
try:
    invoice = create_lnd_invoice(api_url, api_port, amount, memo, macaroon_hex)
    print(invoice)
    print(f"Payment Request: {invoice['payment_request']}")
    print(f"Invoice ID (r_hash): {invoice['r_hash']}")
except Exception as e:
    print(str(e))
