from django.urls import path
from . import views

urlpatterns = [
    path('', views.projetos_view, name='home'),
    path('utilizadores/', views.utilizadores_view, name='utilizadores_view'),
    path('licenciaturas/', views.licenciaturas_view, name='licenciaturas_view'),
    path('ucs/', views.ucs_view, name='ucs_view'),
    path('docentes/', views.docentes_view, name='docentes_view'),
    path('tecnologias/', views.tecnologias_view, name='tecnologias_view'),
    path('formacoes/', views.formacoes_view, name='formacoes_view'),
    path('competencias/', views.competencias_view, name='competencias_view'),
    path('repositorios/', views.repositorios_view, name='repositorios_view'),
    path('tfcs/', views.tfcs_view, name='tfcs_view'),
    path('areas/', views.areas_view, name='areas_view'),
    path('palavras-chave/', views.palavras_chave_view, name='palavras_chave_view'),
    path('makingof/', views.makingof_view, name='makingof_view'),

    
    path('projetos/', views.projetos_view, name='projetos_view'),
    path('projetos/criar/', views.criar_projeto, name='criar_projeto'),
    path('projetos/<int:id>/editar/', views.editar_projeto, name='editar_projeto'),
    path('projetos/<int:id>/apagar/', views.apagar_projeto, name='apagar_projeto'),

    
    path('tecnologias/criar/', views.criar_tecnologia, name='criar_tecnologia'),
    path('tecnologias/<int:id>/editar/', views.editar_tecnologia, name='editar_tecnologia'),
    path('tecnologias/<int:id>/apagar/', views.apagar_tecnologia, name='apagar_tecnologia'),

    
    path('competencias/criar/', views.criar_competencia, name='criar_competencia'),
    path('competencias/<int:id>/editar/', views.editar_competencia, name='editar_competencia'),
    path('competencias/<int:id>/apagar/', views.apagar_competencia, name='apagar_competencia'),

    
    path('formacoes/criar/', views.criar_formacao, name='criar_formacao'),
    path('formacoes/<int:id>/editar/', views.editar_formacao, name='editar_formacao'),
    path('formacoes/<int:id>/apagar/', views.apagar_formacao, name='apagar_formacao'),
]