from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistoForm


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    erro = None

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            erro = "Username ou password incorretos."

    return render(request, 'accounts/login.html', {'form': form, 'erro': erro})


def logout_view(request):
    logout(request)
    return redirect('login')


def registo_view(request):
    form = RegistoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

    return render(request, 'accounts/registo.html', {'form': form})