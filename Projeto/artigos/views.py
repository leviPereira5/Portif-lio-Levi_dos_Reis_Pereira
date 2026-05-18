from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Artigo, Like, Comentario, Avaliacao
from .forms import ArtigoForm, ComentarioForm, AvaliacaoForm


def _e_blogger(user):
    return user.is_authenticated and user.groups.filter(name='bloggers').exists()


def lista_artigos(request):
    artigos = Artigo.objects.order_by('-criado_em')
    return render(request, 'artigos/lista.html', {'artigos': artigos})


def detalhe_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    comentarios = artigo.comentarios.order_by('criado_em')

    ja_gostou = False
    if request.user.is_authenticated:
        ja_gostou = artigo.likes.filter(utilizador=request.user).exists()
    elif request.session.session_key:
        ja_gostou = artigo.likes.filter(sessao=request.session.session_key).exists()

    ja_avaliou = False
    if request.user.is_authenticated:
        ja_avaliou = artigo.avaliacoes.filter(utilizador=request.user).exists()
    elif request.session.session_key:
        ja_avaliou = artigo.avaliacoes.filter(sessao=request.session.session_key).exists()

    return render(request, 'artigos/detalhe.html', {
        'artigo': artigo,
        'comentarios': comentarios,
        'form_comentario': ComentarioForm(),
        'form_avaliacao': AvaliacaoForm(),
        'ja_gostou': ja_gostou,
        'ja_avaliou': ja_avaliou,
        'media_avaliacao': artigo.media_avaliacao(),
        'total_avaliacoes': artigo.avaliacoes.count(),
    })


@login_required
def criar_artigo(request):
    if not _e_blogger(request.user):
        return redirect('lista_artigos')
    form = ArtigoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        artigo = form.save(commit=False)
        artigo.autor = request.user
        artigo.save()
        return redirect('detalhe_artigo', pk=artigo.pk)
    return render(request, 'artigos/form.html', {'form': form, 'titulo': 'Novo Artigo'})


@login_required
def editar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if not _e_blogger(request.user) or artigo.autor != request.user:
        return redirect('lista_artigos')
    form = ArtigoForm(request.POST or None, request.FILES or None, instance=artigo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('detalhe_artigo', pk=artigo.pk)
    return render(request, 'artigos/form.html', {'form': form, 'titulo': 'Editar Artigo'})


@require_POST
def gostar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if request.user.is_authenticated:
        like = Like.objects.filter(artigo=artigo, utilizador=request.user).first()
        if like:
            like.delete()
        else:
            Like.objects.create(artigo=artigo, utilizador=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        sessao = request.session.session_key
        like = Like.objects.filter(artigo=artigo, sessao=sessao).first()
        if like:
            like.delete()
        else:
            Like.objects.create(artigo=artigo, sessao=sessao)
    return redirect('detalhe_artigo', pk=pk)


@require_POST
def comentar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    form = ComentarioForm(request.POST)
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.artigo = artigo
        if request.user.is_authenticated:
            comentario.autor = request.user
            comentario.nome_autor = ''
        else:
            comentario.autor = None
            comentario.nome_autor = form.cleaned_data.get('nome_autor') or 'Anónimo'
        comentario.save()
    return redirect('detalhe_artigo', pk=pk)


@require_POST
def avaliar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    form = AvaliacaoForm(request.POST)
    if not form.is_valid():
        return redirect('detalhe_artigo', pk=pk)

    if request.user.is_authenticated:
        if not artigo.avaliacoes.filter(utilizador=request.user).exists():
            av = form.save(commit=False)
            av.artigo = artigo
            av.utilizador = request.user
            av.save()
    else:
        if not request.session.session_key:
            request.session.create()
        sessao = request.session.session_key
        if not artigo.avaliacoes.filter(sessao=sessao).exists():
            av = form.save(commit=False)
            av.artigo = artigo
            av.sessao = sessao
            av.save()
    return redirect('detalhe_artigo', pk=pk)
