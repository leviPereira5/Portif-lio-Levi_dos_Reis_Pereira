from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    fotografia = models.ImageField(upload_to='artigos/', null=True, blank=True)
    link_externo = models.URLField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artigos')

    def total_likes(self):
        return self.likes.count()

    def media_avaliacao(self):
        resultado = self.avaliacoes.aggregate(media=Avg('pontuacao'))
        return resultado['media']

    def __str__(self):
        return self.titulo


class Like(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='likes')
    utilizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sessao = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f"Like em '{self.artigo}'"


class Comentario(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nome_autor = models.CharField(max_length=100, blank=True)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def get_nome(self):
        if self.autor:
            return self.autor.username
        return self.nome_autor or 'Anónimo'

    def __str__(self):
        return f"Comentário de {self.get_nome()} em '{self.artigo}'"


class Avaliacao(models.Model):
    PONTUACOES = [(i, str(i)) for i in range(1, 6)]

    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='avaliacoes')
    pontuacao = models.IntegerField(choices=PONTUACOES)
    utilizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sessao = models.CharField(max_length=40, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.pontuacao}/5 em '{self.artigo}'"
