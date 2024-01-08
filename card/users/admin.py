from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'is_staff', 'is_active', 'is_superuser', 'access_token']  # Mostrar access_token na lista
    list_filter = ['email', 'is_staff', 'is_active', 'is_superuser']
    readonly_fields = ('access_token',)  # Definir access_token como somente leitura
    fieldsets = (
        (None, {'fields': ('email', 'password', 'access_token')}),  # Incluir access_token aqui
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)  # Ordenar por email em vez de username

admin.site.register(User, UserAdmin)
