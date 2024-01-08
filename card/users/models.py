from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid
from bitcoin_rpc import *
from django.conf import settings
import json
from coins.models import Coin


hd_wallet = settings.HD_WALLET

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        
        # Gera o access_token antes de criar o usuário
        token = uuid.uuid4()
        user = self.model(email=email, access_token=token, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        create_and_load_standard_wallet(str(token))
        
        # Obtém o endereço principal e salva no usuário
        main_address = new_address(str(token), hd_wallet)
        if main_address:
            user.main_address = main_address
            user.save()

        return user


    def create_user_with_token(self, **extra_fields):
        token = uuid.uuid4()
        user = self.model(access_token=token, **extra_fields)  # Set token here
        user.set_unusable_password()
        user.save(using=self._db)

        # Cria uma carteira Bitcoin para o usuário usando o 
        create_and_load_standard_wallet(str(token))

        # Gera um novo endereço e o define como o endereço principal do usuário
        main_address = new_address(str(token), hd_wallet)
        if main_address:
            user.main_address = main_address
            user.save()

        return user, token

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if email is None:
            raise ValueError('Superusuários devem ter um endereço de email.')

        # Cria o superusuário usando o método create_user
        superuser = self.create_user(email, password, **extra_fields)

        # Cria uma carteira HD para o superusuário
        create_and_load_hd_wallet(str(superuser.access_token))

        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    access_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    main_address = models.CharField(max_length=100, null=True, blank=True)
    currency = models.ForeignKey(Coin, on_delete=models.CASCADE, default=1)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.access_token)
