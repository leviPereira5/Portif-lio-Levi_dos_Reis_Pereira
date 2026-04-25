from django.shortcuts import render
from .models import *

def utilizadores_view(request):
    utilizadores = Utilizador.objects.all()
    return render(request, 'portfolio/utilizadores.html', {'utilizadores': utilizadores})


def licenciaturas_view(request):
    licenciaturas = Licenciatura.objects \
        .select_related('utilizador') \
        .all()
    return render(request, 'portfolio/licenciaturas.html', {'licenciaturas': licenciaturas})


def docentes_view(request):
    docentes = Docente.objects.all()
    return render(request, 'portfolio/docentes.html', {'docentes': docentes})


def ucs_view(request):
    ucs = UC.objects \
        .select_related('licenciatura') \
        .prefetch_related('docentes') \
        .all()
    return render(request, 'portfolio/ucs.html', {'ucs': ucs})


def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})


def projetos_view(request):
    projetos = Projeto.objects \
        .select_related('utilizador', 'uc') \
        .prefetch_related('tecnologias', 'competencias') \
        .all()
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})


def formacoes_view(request):
    formacoes = Formacao.objects \
        .prefetch_related('competencias') \
        .all()
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})


def competencias_view(request):
    competencias = Competencia.objects.all()
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})


def repositorios_view(request):
    repositorios = Repositorio.objects \
        .select_related('utilizador', 'projeto') \
        .prefetch_related('tecnologias') \
        .all()
    return render(request, 'portfolio/repositorios.html', {'repositorios': repositorios})



def tfcs_view(request):
    tfcs = TFC.objects \
        .select_related('licenciatura') \
        .prefetch_related(
            'autores',
            'orientadores',
            'tecnologias',
            'areas',
            'palavras_chave'
        ) \
        .all()
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})



def areas_view(request):
    areas = Area.objects.all()
    return render(request, 'portfolio/areas.html', {'areas': areas})


def palavras_chave_view(request):
    palavras_chave = PalavraChave.objects.all()
    return render(request, 'portfolio/palavras_chave.html', {'palavras_chave': palavras_chave})


def makingof_view(request):
    makingofs = MakingOf.objects \
        .select_related('utilizador') \
        .all()
    return render(request, 'portfolio/makingof.html', {'makingofs': makingofs})