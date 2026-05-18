from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .forms import MagicLinkForm, RegistoForm

signer = TimestampSigner()


def login_view(request):
    erro = None
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            username = None
        user = authenticate(request, username=username, password=password) if username else None
        if user is not None:
            login(request, user)
            return redirect("/")
        erro = "Email ou palavra-passe inválidos."
    return render(request, "accounts/login.html", {"erro": erro})


def logout_view(request):
    logout(request)
    return redirect("login")


def registo_view(request):
    form = RegistoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data['email']
        user.save()
        grupo_bloggers, _ = Group.objects.get_or_create(name='bloggers')
        user.groups.add(grupo_bloggers)
        login(request, user)
        return redirect("/")
    return render(request, "accounts/registro.html", {"form": form})


def enviar_magic_link(request):
    form = MagicLinkForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            token = signer.sign(str(user.pk))
            link = request.build_absolute_uri(
                reverse("magic_login", args=[token])
            )
            send_mail(
                "O teu link mágico",
                f"Clica aqui para entrar: {link}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
        return render(request, "accounts/magic_link_pedido.html", {"enviado": True})
    return render(request, "accounts/magic_link_pedido.html", {"form": form})


def magic_login(request, token):
    try:
        user_id = signer.unsign(token, max_age=600)
        user = User.objects.get(pk=user_id)
        login(request, user)
        return redirect("/")
    except (BadSignature, SignatureExpired, User.DoesNotExist):
        return render(request, "accounts/magic_link_erro.html")
