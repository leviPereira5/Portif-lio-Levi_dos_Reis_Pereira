from django.contrib import admin
from .models import Artigo, Like, Comentario

admin.site.register(Artigo)
admin.site.register(Like)
admin.site.register(Comentario)
