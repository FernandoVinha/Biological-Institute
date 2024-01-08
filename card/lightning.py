from pylightning import LightningRpc

# Caminho para o arquivo de socket do LND
LND_SOCKET = "/root/.lnd/data/chain/bitcoin/mainnet/rpc.sock"

# Crie uma instância da classe LightningRpc para se conectar ao seu nó LND
lnd = LightningRpc(LND_SOCKET)

# Consultar informações de saldo
info = lnd.getinfo()
print("Informações do canal:")
print(f"ID do Nó: {info['id']}")
print(f"Saldo Total: {info['msatoshi_fees_collected']} msatoshis")
print(f"Altura Atual do Bloco: {info['blockheight']}")

# Criar uma fatura (invoice)
invoice = lnd.invoice(1000, "Descrição do pagamento")
print("\nFatura criada:")
print(f"Rótulo: {invoice['label']}")
print(f"Valor: {invoice['msatoshi']} msatoshis")
print(f"Pagamento Hash: {invoice['payment_hash']}")
print(f"Prazo de Pagamento: {invoice['expires_at']}")

# Pagar uma fatura
payment_hash = invoice['payment_hash']
payment_request = invoice['bolt11']
print("\nPagando a fatura...")
result = lnd.pay(payment_request)
if result['status'] == 'complete':
    print("Pagamento bem-sucedido!")
else:
    print("Falha no pagamento:", result['status'])

# Listar canais
channels = lnd.listchannels()
print("\nCanais Abertos:")
for channel in channels['channels']:
    print(f"ID do Canal: {channel['short_channel_id']}")
    print(f"Capacidade: {channel['satoshis']} satoshis")
    print(f"Status: {channel['state']}\n")
