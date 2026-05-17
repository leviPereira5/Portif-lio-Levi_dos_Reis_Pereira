from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Artigo, Like, Comentario
from .forms import ArtigoForm, ComentarioForm


def _e_autor(user):
    return user.is_authenticated and user.groups.filter(name='autores').exists()


@login_required
def lista_artigos(request):
    artigos = Artigo.objects.order_by('-criado_em')
    return render(request, 'artigos/lista.html', {'artigos': artigos})


@login_required
def detalhe_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    comentarios = artigo.comentarios.order_by('criado_em')

    ja_gostou = False
    if request.user.is_authenticated:
        ja_gostou = artigo.likes.filter(utilizador=request.user).exists()
    elif request.session.session_key:
        ja_gostou = artigo.likes.filter(sessao=request.session.session_key).exists()

    return render(request, 'artigos/detalhe.html', {
        'artigo': artigo,
        'comentarios': comentarios,
        'form_comentario': ComentarioForm(),
        'ja_gostou': ja_gostou,
    })


@login_required
def criar_artigo(request):
    if not _e_autor(request.user):
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
    if not _e_autor(request.user) or artigo.autor != request.user:
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


@login_required
@require_POST
def comentar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    form = ComentarioForm(request.POST)
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.artigo = artigo
        comentario.autor = request.user
        comentario.save()
    return redirect('detalhe_artigo', pk=pk)
