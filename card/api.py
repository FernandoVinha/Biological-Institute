import requests

# URL da API para registrar um usuário
url = 'http://localhost:8000/api/register/'  # Substitua pelo URL correto do seu servidor

# Dados do usuário a ser registrado
user_data = {
    'email': 'usuario2@example.com',
    'password': 'senha123$',
    'password2': 'senha123$'  # Confirmação da senha
}

# Fazendo a solicitação POST para a API
response = requests.post(url, data=user_data)

# Imprimindo a resposta da API
print(response.status_code)
print(response.json())
