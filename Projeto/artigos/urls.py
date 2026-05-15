from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_artigos, name='lista_artigos'),
    path('criar/', views.criar_artigo, name='criar_artigo'),
    path('<int:pk>/', views.detalhe_artigo, name='detalhe_artigo'),
    path('<int:pk>/editar/', views.editar_artigo, name='editar_artigo'),
    path('<int:pk>/gostar/', views.gostar_artigo, name='gostar_artigo'),
    path('<int:pk>/comentar/', views.comentar_artigo, name='comentar_artigo'),
]
