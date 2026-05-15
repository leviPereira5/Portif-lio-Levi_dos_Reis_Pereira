from django.db import models
from django.contrib.auth.models import User
import secrets
from datetime import timedelta
from django.utils import timezone


class MagicToken(models.Model):
    """Guarda o token temporário para autenticação por link mágico."""
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='magic_token')
    token = models.CharField(max_length=100, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def é_válido(self):
        """Token expira ao fim de 15 minutos."""
        return timezone.now() < self.criado_em + timedelta(minutes=15)

    @classmethod
    def criar_para(cls, user):
        """Cria (ou renova) um token para o utilizador."""
        cls.objects.filter(user=user).delete()
        return cls.objects.create(
            user=user,
            token=secrets.token_urlsafe(32)
        )

    def __str__(self):
        return f"Token de {self.user.username}"