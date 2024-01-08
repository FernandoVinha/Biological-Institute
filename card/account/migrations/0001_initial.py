# Generated by Django 4.2.7 on 2023-12-28 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source', models.CharField(choices=[('bitcoin', 'Bitcoin'), ('internal', 'Internal'), ('lightning', 'Lightning')], default='internal', max_length=10)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('mensagem', models.TextField(blank=True, null=True)),
                ('bitcoin_address', models.CharField(blank=True, max_length=255, null=True)),
                ('lightning_address', models.CharField(blank=True, max_length=255, null=True)),
                ('received', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('paid', 'Pago'), ('partially_paid', 'Parcialmente Pago'), ('not_paid', 'Não Pago'), ('unconfirmed', 'Não Confirmado')], default='not_paid', max_length=20)),
                ('lightning_address', models.CharField(blank=True, max_length=255)),
                ('r_hash', models.CharField(blank=True, max_length=255, null=True)),
                ('bitcoin_address', models.CharField(blank=True, max_length=255, null=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coins.coin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
