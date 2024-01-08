import requests
import json
import urllib3
from django.conf import settings

# Suprimir avisos de requisições HTTPS inseguras (para desenvolvimento/testes)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Exemplo de uso da função
api_url = "localhost"
api_port = "8081"#é a porta que eu defin para api do lnd

def create_lnd_invoice(api_url, api_port, memo=None):
    url = f"https://{api_url}:{api_port}/v1/invoices"
    headers = {
        'Content-Type': 'application/json',
        'Grpc-Metadata-macaroon': settings.LND_MACAROON_HEX,
    }
    invoice_data = {
        "memo": memo if memo else "",  # Descrição da invoice (opcional)
    }

    response = requests.post(url, headers=headers, data=json.dumps(invoice_data), verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao criar a invoice: {response.status_code} {response.text}")
