from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Outras rotas do seu aplicativo
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
]
