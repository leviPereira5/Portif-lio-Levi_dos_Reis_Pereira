from django.contrib import admin
from .models import Artigo, Like, Comentario, Avaliacao

admin.site.register(Artigo)
admin.site.register(Like)
admin.site.register(Comentario)
admin.site.register(Avaliacao)
