from django.urls import path
from . import views

urlpatterns = [
    path('', views.projetos_view, name='home'),  # página inicial
    path('utilizadores/', views.utilizadores_view, name='utilizadores_view'),
    path('licenciaturas/', views.licenciaturas_view, name='licenciaturas_view'),
    path('ucs/', views.ucs_view, name='ucs_view'),
    path('docentes/', views.docentes_view, name='docentes_view'),
    path('tecnologias/', views.tecnologias_view, name='tecnologias_view'),
    path('projetos/', views.projetos_view, name='projetos_view'),
    path('formacoes/', views.formacoes_view, name='formacoes_view'),
    path('competencias/', views.competencias_view, name='competencias_view'),
    path('repositorios/', views.repositorios_view, name='repositorios_view'),
    path('tfcs/', views.tfcs_view, name='tfcs_view'),
    path('areas/', views.areas_view, name='areas_view'),
    path('palavras-chave/', views.palavras_chave_view, name='palavras_chave_view'),
    path('makingof/', views.makingof_view, name='makingof_view'),
]