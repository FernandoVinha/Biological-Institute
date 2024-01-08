from django.db import models
import requests
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.files.base import ContentFile
import os

# Create your models here.
class Coin(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    precision = models.PositiveSmallIntegerField()
    _type = models.CharField(max_length=50)

    def __str__(self):
        return self.code
    
@receiver(post_migrate)
def populate_currency(sender, **kwargs):
    # Check if any Coin objects already exist
    if Coin.objects.exists():
        # If they do, return immediately and do nothing
        return

    url = "https://bisq.markets/api/currencies"
    # Make the HTTP request
    response = requests.get(url)
    # Extract the coin data
    json_dict = response.json()
    # Check if the request was successful
    if response.status_code == 200:
        for key, value in json_dict.items():
            Coin.objects.create(code=value['code'], name=value['name'], precision=value['precision'], _type=value['_type'])
