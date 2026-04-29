from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import ProjetoForm, TecnologiaForm, CompetenciaForm, FormacaoForm

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
        .prefetch_related('autores', 'orientadores', 'tecnologias', 'areas', 'palavras_chave') \
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


# TODOS OS METODOS CRUD AI PARA BAIXO :)

def criar_projeto(request):
    form = ProjetoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('projetos_view')
    return render(request, 'portfolio/form.html', {'form': form, 'titulo': 'Criar Projeto', 'voltar': 'projetos_view'})

def editar_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)
    if form.is_valid():
        form.save()
        return redirect('projetos_view')
    return render(request, 'portfolio/form.html', {'form': form, 'titulo': 'Editar Projeto', 'voltar': 'projetos_view'})

def apagar_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    if request.method == 'POST':
        projeto.delete()
        return redirect('projetos_view')
    return render(request, 'portfolio/confirmar_apagar.html', {'objeto': projeto, 'voltar': 'projetos_view'})


def criar_tecnologia(request):
    form = TecnologiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('tecnologias_view')
    return render(request, 'portfolio/form.html', {'form': form, 'titulo': 'Criar Tecnologia', 'voltar': 'tecnologias_view'})

def editar_tecnologia(request, id):
    tecnologia = get_object_or_404(Tecnologia, id=id)
    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=tecnologia)
    if form.is_valid():
        form.save()
        return redirect('tecnologias_view')
    return render(request, 'portfolio/form.html', {'form': form, 'titulo': 'Editar Tecnologia', 'voltar': 'tecnologias_view'})

def apagar_tecnologia(request, id):
    tecnologia = get_object_or_404(Tecnologia, id=id)
    if request.method == 'POST':
        tecnologia.delete()
        return redirect('tecnologias_view')
    return render(request, 'portfolio/confirmar_apagar.html', {'objeto': tecnologia, 'voltar': 'tecnologias_view'})



def criar_competencia(request):
    form = CompetenciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('competencias_view')
    return render(request, 'portfolio/form.html', {'form': form, 'titulo': 'Criar Competência', 'voltar': 'competencias_view'})

def editar_competencia(request, id):
    competencia = get_object_or_404(Competencia, id=id)
    form = CompetenciaForm(request.POST or None, instance=competencia)
    if form.is_valid():
        form.save()
        return redirect('competencias_view')
    return render(request, 'portfolio/form.html', {'form': form, 'titulo': 'Editar Competência', 'voltar': 'competencias_view'})

def apagar_competencia(request, id):
    competencia = get_object_or_404(Competencia, id=id)
    if request.method == 'POST':
        competencia.delete()
        return redirect('competencias_view')
    return render(request, 'portfolio/confirmar_apagar.html', {'objeto': competencia, 'voltar': 'competencias_view'})


def criar_formacao(request):
    form = FormacaoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('formacoes_view')
    return render(request, 'portfolio/form.html', {'form': form, 'titulo': 'Criar Formação', 'voltar': 'formacoes_view'})

def editar_formacao(request, id):
    formacao = get_object_or_404(Formacao, id=id)
    form = FormacaoForm(request.POST or None, instance=formacao)
    if form.is_valid():
        form.save()
        return redirect('formacoes_view')
    return render(request, 'portfolio/form.html', {'form': form, 'titulo': 'Editar Formação', 'voltar': 'formacoes_view'})

def apagar_formacao(request, id):
    formacao = get_object_or_404(Formacao, id=id)
    if request.method == 'POST':
        formacao.delete()
        return redirect('formacoes_view')
    return render(request, 'portfolio/confirmar_apagar.html', {'objeto': formacao, 'voltar': 'formacoes_view'})