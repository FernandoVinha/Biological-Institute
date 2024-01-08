from django.db import models
from users.models import User
from coins.models import Coin  # Import the Coin model
import uuid
import config
from bitcoin_rpc import *
from lnd import *
from django.conf import settings

SOURCE = [
    ('bitcoin', 'Bitcoin'),
    ('internal', 'Internal'),
    ('lightning', 'Lightning'),
]

TYPE = [
    ('received', 'Received'),
    ('spent', 'Spent'),
]

class Transfer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=10, choices=SOURCE, default="internal")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    mensagem = models.TextField(blank=True, null=True)
    bitcoin_address = models.CharField(max_length=255, blank=True, null=True)
    lightning_address = models.CharField(max_length=255, blank=True, null=True)
    received = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transfer - ID: {self.id}, User: {self.user}, Status: {self.status}, Amount: {self.valor}"

class Invoice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20,
        choices=(
            ('paid', 'Pago'),
            ('partially_paid', 'Parcialmente Pago'),
            ('not_paid', 'Não Pago'),
            ('unconfirmed', 'Não Confirmado')
        ),
        default='not_paid'
    )
    currency = models.ForeignKey(Coin, on_delete=models.CASCADE)
    lightning_address = models.CharField(max_length=255, blank=True)
    r_hash = models.CharField(max_length=255, blank=True, null=True)
    bitcoin_address = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.currency_id:
            self.currency = self.user.currency

        if not self.pk:
            memo = f"{self.currency.code} - Valor: {self.amount}"
            try:
                lnd_invoice = create_lnd_invoice(settings.LND_API_URL, settings.LND_API_PORT, memo=memo)
                self.lightning_address = lnd_invoice.get('payment_request')
                self.r_hash = lnd_invoice.get('r_hash')
            except Exception as e:
                print(f"Erro ao criar fatura LND: {e}")

        if not self.bitcoin_address:
            new_address_result = new_address(self.user.access_token, settings.HD_WALLET)

            print(new_address_result)
            if new_address_result is not None:
                self.bitcoin_address = new_address_result

        super().save(*args, **kwargs)

    def __str__(self):
        status_pagamento = dict(self.payment_status.choices).get(self.payment_status)
        return f"Usuário: {self.user}, Valor: {self.amount}, Status: {status_pagamento}"

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20,
        choices=(
            ('paid', 'Pago'),
            ('partially_paid', 'Parcialmente Pago'),
            ('not_paid', 'Não Pago'),
            ('unconfirmed', 'Não Confirmado')
        ),
        default='not_paid'
    )
    currency = models.ForeignKey(Coin, on_delete=models.CASCADE)
    lightning_address = models.CharField(max_length=255, blank=True)
    r_hash = models.CharField(max_length=255, blank=True, null=True)
    bitcoin_address = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Define a moeda do Invoice com base na moeda do usuário, se ainda não estiver definida
        if not self.pk and not self.currency_id:
            self.currency = self.user.currency

        # Se a Invoice está sendo criada pela primeira vez, gera uma fatura LND
        if not self.pk:
            memo = f"{self.currency.code} - Valor: {self.amount}"
            try:
                lnd_invoice = create_lnd_invoice(settings.LND_API_URL, settings.LND_API_PORT, memo=memo)
                self.lightning_address = lnd_invoice.get('payment_request')
                self.r_hash = lnd_invoice.get('r_hash')
            except Exception as e:
                print(f"Erro ao criar fatura LND: {e}")

        if not self.bitcoin_address:
            print("usuário: " + str(self.user.access_token))
            print("endereço HD: " + settings.HD_WALLET)
            new_address_result = new_address(self.user.access_token, settings.HD_WALLET)
            if new_address_result is not None:
                self.bitcoin_address = new_address_result  # Atribua diretamente o endereço

        super().save(*args, **kwargs)

    def __str__(self):
        status_pagamento = dict(self.payment_status.choices).get(self.payment_status)
        return f"Usuário: {self.user}, Valor: {self.amount}, Status: {status_pagamento}"
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20,
        choices=(
            ('paid', 'Pago'),
            ('partially_paid', 'Parcialmente Pago'),
            ('not_paid', 'Não Pago'),
            ('unconfirmed', 'Não Confirmado')
        ),
        default='not_paid'
    )
    currency = models.ForeignKey(Coin, on_delete=models.CASCADE)
    lightning_address = models.CharField(max_length=255, blank=True)
    r_hash = models.CharField(max_length=255, blank=True, null=True)
    bitcoin_address = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Defina a moeda do Invoice com base na moeda do usuário, se ainda não estiver definida
        if not self.pk and not self.currency_id:
            self.currency = self.user.currency

        # Se a Invoice está sendo criada pela primeira vez, gera uma fatura LND
        if not self.pk:
            memo = f"{self.currency.code} - Valor: {self.amount}"  # Memo personalizado com código da moeda e valor
            try:
                lnd_invoice = create_lnd_invoice(settings.LND_API_URL, settings.LND_API_PORT, memo=memo)
                self.lightning_address = lnd_invoice.get('payment_request')
                self.r_hash = lnd_invoice.get('r_hash')
            except Exception as e:
                # Trate quaisquer exceções, possivelmente registrando-as
                print(f"Erro ao criar fatura LND: {e}")
                # Generate a new Bitcoin address when saving if one doesn't exist
        if not self.bitcoin_address:
            new_address_result = new_address(self.user.access_token, settings.HD_WALLET)
            if new_address_result is not None:
                self.bitcoin_address, _ = new_address_result


        super().save(*args, **kwargs)

    def __str__(self):
        status_pagamento = dict(self.payment_status.choices).get(self.payment_status)
        return f"Usuário: {self.user}, Valor: {self.amount}, Status: {status_pagamento}"