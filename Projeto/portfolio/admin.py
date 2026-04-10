from django.contrib import admin
from .models import *

@admin.register(Utilizador)
class UtilizadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome', 'email')


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'instituicao', 'duracao_anos')
    search_fields = ('nome', 'sigla')
    list_filter = ('instituicao',)


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome',)


@admin.register(UC)
class UCAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'ano', 'semestre')
    list_filter = ('ano', 'semestre')
    search_fields = ('nome', 'codigo')


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'nivel_preferencia')
    list_filter = ('tipo',)
    search_fields = ('nome',)


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'uc')
    search_fields = ('titulo',)
    list_filter = ('data',)


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'instituicao', 'data_inicio', 'data_fim')


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'nivel')


@admin.register(Repositorio)
class RepositorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'visibilidade', 'data_criacao')


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano', 'classificacao')
    list_filter = ('ano',)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(PalavraChave)
class PalavraChaveAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ('id', 'data')