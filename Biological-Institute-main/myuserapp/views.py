from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirecionar para a página inicial após o login
        else:
            messages.error(request, 'E-mail ou senha inválidos')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')  # Redirecione para a página desejada após o logout